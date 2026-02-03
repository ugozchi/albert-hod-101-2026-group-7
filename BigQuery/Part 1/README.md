# Deliveroo Plus : Subscription Tagging (SQL Only)

## File Structure

```
BigQuery/Part 1/Queries/
├── table_creation.sql                                     # Step 0
├── Step1_Subscription_block_detection.sql                 # Step 1
├── Step2_block_level_aggregation.sql                      # Step 2
├── Step3_Subscription_tagging.sql                         # Step 3
├── Step4.1_quick_use_case_answer.sql                      # Step 4.1
├── Step4.2_quick_user_case_answer.sql                     # Step 4.2
├── Scalability_query.sql                                  # Scalability version
├── Checking_query.sql                                     # Validation queries
├── TDD1_never_subscribed_if_delivery_is_chargeable.sql    # Testing and validation queries 1
├── TDD2_if_subscribed_then_start_end_not_NULL.sql         # Testing and validation queries 2
├── TDD3_if_subscribed_datetime_in_[start, end].sql        # Testing and validation queries 3
└── TDD4_Strict_consistency_threshold_=_block_stats.sql    # Testing and validation queries 4
```

---

## 1) Project Objective

Identify **Deliveroo Plus subscription periods** using transactional data only (no explicit subscription start/cancel events).

Synthetic dataset: one row per order, with `id_customer_synth`, `order_datetime_synth`, and `is_free_delivery`. Goal: reconstruct subscription periods from incomplete history while keeping the logic explainable, scalable, and suitable for business analysis.

---

## 2) Business Context and Constraints

Deliveroo Plus: fixed monthly fee (~10€) for free deliveries (~3€ saved per order).

**Client question (Foxintelligence):** Tag Deliveroo Plus customers in the DB to analyze how the loyalty program changes behavior.

**Constraint:** In 2020, no subscription/cancellation emails; we only parse delivery fee from emails.

**Approximation:** ≥3 consecutive orders with free delivery → subscriber; those orders and following free-delivery orders count as subscription.

**Scalability:** Threshold (3) must be easy to change (e.g. to 20) via one parameter.

---

## 3) Our Approach and Reasoning

**Methodology:** Reason on **observed behavior** (when does behavior become compatible with a subscription?) and **consecutive order sequences** rather than individual orders.

**Pipeline in steps:** Readability, debuggability, maintainability, explainability. Each step has one clear responsibility.

**Order:** (0) Prepare data, compare to previous order → (1) Identify blocks of consecutive same-status orders → (2) Block-level stats → (3) Tag subscriptions → (4) Enrich for interpretability. Each step builds on the previous.

---

## 4) Data Overview

**Source:** `assignment_data.synthetic_deliveroo_plus_dataset` (immutable).

**Intermediate (group_7):** `tmp_deliveroo_ordered`, `tmp_deliveroo_blocks`, `tmp_deliveroo_block_stats`.

**Output:** `final_dataset` (main deliverable), `Scalability_dataset` (configurable threshold).

---

## 5) Implementation

### Step 0) Order History Preparation  
**File:** `table_creation.sql` → `tmp_deliveroo_ordered`  
Chronological order per customer; `LAG()` for `prev_is_free_delivery`. Foundation for detecting delivery-fee changes.

### Step 1) Subscription Block Detection  
**File:** `Step1_Subscription_block_detection.sql` → `tmp_deliveroo_blocks`  
Segment into blocks where `is_free_delivery` is constant; new block when it changes. `CASE` + cumulative sum for `block_id`. Supports multiple subscriptions per customer.

### Step 2) Block-Level Aggregation  
**File:** `Step2_block_level_aggregation.sql` → `tmp_deliveroo_block_stats`  
Per (customer, block_id): `block_size`, `block_start_datetime`, `block_end_datetime`. Window functions with `PARTITION BY id_customer_synth, block_id`.

### Step 3) Subscription Tagging  
**File:** `Step3_Subscription_tagging.sql` → `final_dataset`  
Rule: subscription if `is_free_delivery = 1` and `block_size >= threshold` (default 3). Set subscription start/end from block boundaries; else NULL.

### Step 4) Visual Enrichment  
**4.1** `Step4.1_quick_use_case_answer.sql`: add `subscription_phase` (BEFORE / DURING / AFTER / NO_SUBSCRIPTION_INFO).  
**4.2** `Step4.2_quick_user_case_answer.sql`: add `days_from_subscription_start` for timeline analysis.

---

## 6) Scalability

**File:** `Scalability_query.sql` → `Scalability_dataset`  
Single parameter: `SELECT 3 AS subscription_threshold`. Change this value only; entire pipeline adapts. Supports sensitivity analysis and evolving business rules.

---

## 7) Test-Driven Development (TDD)

Each test is a SQL query that must return **zero rows** if the logic is correct.

- **TDD1** `TDD1_never_subscribed_if_delivery_is_chargeable.sql`: paid delivery → not subscription.
- **TDD2** `TDD2_if_subscribed_then_start_end_not_NULL.sql`: subscription orders must have start/end dates.
- **TDD3** `TDD3_if_subscribed_datetime_in_[start, end].sql`: order datetime must be within subscription period.
- **TDD4** `TDD4_Strict_consistency_threshold_=_block_stats.sql`: tagging consistent with block stats and threshold.

---

## 8) Answering the Business Question

**Client need:** Analyze how Deliveroo Plus changes behavior without explicit subscription events.

**Solution:** Reconstruct periods from repeated free deliveries. Enables before/during/after comparison, frequency/retention analysis, churn patterns. `final_dataset` is BI-ready (subscription flag, boundaries, `subscription_phase`, `days_from_subscription_start`).

**Validity:** Explicit rule, behavior-based proxy (free delivery), multiple subscriptions supported, TDD validation. Threshold is configurable for sensitivity and evolution.

**Business value:** Quantify loyalty impact, benchmark strategy, actionable insights despite incomplete history. Pragmatic and trustworthy for decision-making.
