# Deliveroo Plus — Subscription Tagging (SQL Only)

## 1) Project Objective

The objective of this project is to identify **Deliveroo Plus subscription periods** using transactional data only, without relying on explicit subscription start or cancellation events.

We work with a synthetic dataset where each row represents one Deliveroo order, enriched with:
- a customer identifier (`id_customer_synth`),
- an order datetime (`order_datetime_synth`),
- a binary indicator (`is_free_delivery`) specifying whether the delivery fee was waived.

The core challenge is to reconstruct subscription periods from incomplete historical information, while ensuring that the resulting logic remains:
- explainable,
- scalable,
- and suitable for business analysis.

---

## 2) Business Context and Constraints

Deliveroo Plus is a loyalty program where customers pay a fixed monthly fee (approximately 10€) to benefit from free deliveries, which typically save around 3€ per order.

**The client's question:** As a Foxintelligence head of data, a client who is a competitor of Deliveroo is asking if we are able to tag Deliveroo Plus customers in the database in order to analyze how the loyalty program changes customer behavior.

**The constraint:** Back in 2020, customers did not receive a subscription email when they joined nor a cancellation email when they left. However, we parse the delivery fee in the email.

**The agreed approximation:** The client agrees that we can make an approximation by considering that a customer for whom we observe at least 3 orders in a row without paying a delivery fee is a Deliveroo Plus subscriber, and that all these orders and the subsequent ones without a delivery fee would be explained by the subscription.

**Scalability requirement:** The threshold of 3 is arbitrary. We need to ensure that the code can handle a threshold of 20 instead of 3 very easily (e.g., with a find and replace command or a single parameter change).

---

## 3) Our Approach and Reasoning

### 3.1) Why We Chose This Methodology

We decided to reason in terms of **observed behavior** rather than trying to infer theoretical subscription dates. Instead of asking "when did the customer subscribe?", we asked "when does the customer's behavior become compatible with a subscription?"

This naturally led us to think in terms of **consecutive sequences of orders** rather than individual orders taken in isolation.

### 3.2) Why We Structured the Pipeline in Steps

We chose to break down the problem into explicit, sequential steps rather than writing a single complex query. This design decision was motivated by several considerations:

- **Readability:** Each step has a single, clear responsibility that can be understood independently.
- **Debuggability:** If something goes wrong, we can validate each intermediate table and identify exactly where the issue occurs.
- **Maintainability:** Future modifications (e.g., changing the threshold) are easier when the logic is modular.
- **Explainability:** We can explain our reasoning step by step, which is crucial for business stakeholders and reviewers.

### 3.3) Why This Order of Steps

The order of steps follows a logical progression:

1. **First**, we need to prepare the data in chronological order and compare each order to the previous one (Step 0).
2. **Then**, we can identify homogeneous blocks of consecutive orders (Step 1).
3. **Next**, we compute block-level statistics that will allow us to apply the business rule (Step 2).
4. **Finally**, we tag subscriptions based on these statistics (Step 3).
5. **Additionally**, we enrich the output for better interpretability (Step 4).

This sequence ensures that each step builds on the previous one, and that we never need to go back and modify earlier steps.

---

## 4) Data Overview

### 4.1) Source Dataset
- `assignment_data.synthetic_deliveroo_plus_dataset`

This dataset is treated as immutable input data.

### 4.2) Intermediate Tables (created in `group_7`)
- `tmp_deliveroo_ordered`
- `tmp_deliveroo_blocks`
- `tmp_deliveroo_block_stats`

These tables make the logic transparent and debuggable, instead of hiding all transformations in a single query.

### 4.3) Output Tables
- `final_dataset`: main deliverable
- `Scalability_dataset`: identical logic with a configurable threshold

---

## 5) Step-by-Step Implementation

### 5.1) Step 0 — Order History Preparation

**Query file:** `table_creation.sql`  
**Output table:** `tmp_deliveroo_ordered`

**What we do:**
We prepare a clean, chronological view of each customer's order history. Orders are partitioned by customer and ordered by datetime. We use the `LAG()` window function to retrieve the delivery status of the previous order.

**Why this step is necessary:**
Subscription detection relies on identifying **changes** in delivery fee status. Without access to the previous order's status, we cannot detect transitions between paid and free deliveries. This step is the foundation for all subsequent segmentation logic.

**How it works:**
- For each customer, we sort orders chronologically.
- We compute `prev_is_free_delivery` using `LAG(is_free_delivery) OVER (PARTITION BY id_customer_synth ORDER BY order_datetime_synth)`.
- The first order of each customer has `prev_is_free_delivery = NULL`.

**Expected result:**
A table with the same structure as the source, plus a `prev_is_free_delivery` column that allows us to compare each order to the previous one.

---

### 5.2) Step 1 — Subscription Block Detection

**Query file:** `Step1_Subscription_block_detection.sql`  
**Output table:** `tmp_deliveroo_blocks`

**What we do:**
We segment each customer's order history into consecutive blocks where the delivery fee status remains constant. A new block starts whenever `is_free_delivery` changes compared to the previous order.

**Why we thought this approach was essential:**
The business rule requires identifying **consecutive** free deliveries. We cannot simply count isolated free deliveries; we need to identify continuous sequences. This step transforms the problem from "individual order analysis" to "block-level analysis."

**How we handle multiple subscriptions:**
By creating blocks that restart whenever the status changes, we naturally support multiple subscription periods per customer. Each time a customer transitions from paid to free delivery (and meets the threshold), it creates a new subscription period.

**How it works:**
- We use a `CASE` statement to detect when a new block should start:
  - If `prev_is_free_delivery IS NULL` (first order), we start block 1.
  - If `is_free_delivery != prev_is_free_delivery`, we start a new block.
  - Otherwise, we stay in the same block.
- We use a cumulative sum (`SUM(...) OVER (...)`) to generate a `block_id` that increments each time a new block starts.

**Expected result:**
A table where each order has a `block_id`. For a given customer, `block_id` will look like: 1, 1, 1, 2, 2, 3, 3... Each change in delivery status increments the block_id.

---

### 5.3) Step 2 — Block-Level Aggregation

**Query file:** `Step2_block_level_aggregation.sql`  
**Output table:** `tmp_deliveroo_block_stats`

**What we do:**
For each `(customer, block_id)` pair, we compute:
- `block_size`: number of orders in the block,
- `block_start_datetime`: datetime of the first order,
- `block_end_datetime`: datetime of the last order.

**Why this step is crucial:**
The business rule depends on the **number of consecutive free deliveries**, not on isolated events. We need block-level statistics to evaluate whether a block qualifies as a subscription. Additionally, we need the start and end datetimes to populate the final output fields.

**How it works:**
- We use window functions with `PARTITION BY id_customer_synth, block_id` to compute statistics that are constant within each block.
- `COUNT(*) OVER (...)` gives us the block size.
- `MIN(order_datetime_synth) OVER (...)` and `MAX(order_datetime_synth) OVER (...)` give us the block boundaries.

**Expected result:**
A table where all orders in the same block share the same `block_size`, `block_start_datetime`, and `block_end_datetime` values.

---

### 5.4) Step 3 — Subscription Tagging

**Query file:** `Step3_Subscription_tagging.sql`  
**Output table:** `final_dataset`

**What we do:**
We tag each order as being placed during a subscription or not, based on the block-level statistics.

**Decision rule:**
An order is tagged as part of a subscription if:
- `is_free_delivery = 1`, and
- `block_size >= subscription_threshold` (default: 3).

**Why we apply the rule at this stage:**
By this point, we have all the information we need:
- We know which block each order belongs to,
- We know the size of each block,
- We know the temporal boundaries of each block.

Applying the rule here is straightforward and transparent.

**How it works:**
- For qualifying blocks (free delivery + size >= threshold):
  - `is_order_made_during_subscription = 1`,
  - `current_subscription_start_datetime = block_start_datetime`,
  - `current_subscription_end_datetime = block_end_datetime`.
- For non-qualifying blocks:
  - `is_order_made_during_subscription = 0`,
  - subscription start/end fields are set to `NULL`.

**Expected result:**
A table where each order is enriched with subscription information. Orders in qualifying free-delivery blocks are tagged as subscriptions, with consistent start/end datetimes across all orders in the same block.

---

### 5.5) Step 4 — Visual Enrichment

After identifying subscription periods (Steps 1-3), we introduced an additional step to make the final dataset more readable and business-friendly. This step does not alter the subscription logic; it enhances interpretability.

#### 5.5.1) Step 4.1 — Subscription Phase Classification

**Query file:** `Step4.1_quick_use_case_answer.sql`

**What we do:**
We add a `subscription_phase` column that classifies each order as:
- `BEFORE`: placed before a subscription starts,
- `DURING`: placed during an active subscription,
- `AFTER`: placed after a subscription has ended,
- `NO_SUBSCRIPTION_INFO`: no subscription context available.

**Why we added this:**
Managers and analysts need to understand customer behavior relative to subscriptions without manually interpreting start/end datetimes. This categorical variable makes segmentation and dashboarding much easier.

**How it works:**
- We use window functions to find:
  - the next subscription start date after each order,
  - the most recent subscription end date before each order.
- We compare the order datetime to these boundaries to determine the phase.

**Expected result:**
A categorical column that immediately shows where each order falls in the customer's subscription lifecycle.

#### 5.5.2) Step 4.2 — Subscription Timeline Indicator

**Query file:** `Step4.2_quick_user_case_answer.sql`

**What we do:**
We add a `days_from_subscription_start` column that indicates how many days have elapsed since the start of the subscription for each order.

**Why we added this:**
This relative timeline allows us to analyze how customer behavior evolves during a subscription (e.g., engagement in the first week vs. later weeks). It makes patterns visible even in simple tabular views.

**How it works:**
- For orders during a subscription: `DATE_DIFF(DATE(order_datetime_synth), DATE(current_subscription_start_datetime), DAY)`.
- For orders outside subscriptions: `NULL`.

**Expected result:**
A numerical column where day 0 corresponds to the first order of a subscription, and subsequent orders are positioned along a relative timeline.

---

## 6) Scalability

**Query file:** `Scalability_query.sql`  
**Output table:** `Scalability_dataset`

**How we ensure scalability:**
The subscription threshold is defined **once**, in a single parameter:

```sql
SELECT 3 AS subscription_threshold
```

All subscription logic depends on this parameter. Changing the threshold (e.g., from 3 to 20) requires modifying only this value, without rewriting the rest of the pipeline.

**Why this design:**
- It avoids hard-coded logic scattered throughout the code.
- It supports sensitivity analysis (testing different thresholds).
- It aligns with real-world scenarios where business definitions evolve.

**How a manager would change it:**
Simply modify the `subscription_threshold` value in the `CROSS JOIN` subquery. The entire tagging logic automatically adapts.

---

## 7) Test-Driven Development (TDD)

To ensure the correctness and robustness of the tagging logic, we implemented several SQL-based consistency checks.

**Our TDD approach:**
Each test is written as a SQL query expected to return **zero rows** if the logic is correct. If a test returns any rows, it indicates a logical inconsistency that needs to be fixed.

### 7.1) Test 1 — Paid Deliveries Cannot Be Subscriptions

**Query file:** `TDD1_never_subscribed_if_delivery_is_chargeable.sql`

**What it checks:**
Orders with `is_free_delivery = 0` cannot be tagged as subscription orders.

**Why this matters:**
This is a fundamental business rule: if the customer paid for delivery, they cannot be considered subscribed.

### 7.2) Test 2 — Subscription Orders Must Have Start/End Dates

**Query file:** `TDD2_if_subscribed_then_start_end_not_NULL.sql`

**What it checks:**
If an order is tagged as `is_order_made_during_subscription = 1`, then both `current_subscription_start_datetime` and `current_subscription_end_datetime` must be non-null.

**Why this matters:**
Subscription periods must have well-defined boundaries. Missing dates would indicate a logic error.

### 7.3) Test 3 — Order Datetime Must Be Within Subscription Period

**Query file:** `TDD3_if_subscribed_datetime_in_[start, end].sql`

**What it checks:**
For subscription orders, the `order_datetime_synth` must fall between `current_subscription_start_datetime` and `current_subscription_end_datetime`.

**Why this matters:**
This ensures temporal consistency: an order cannot be tagged as "during subscription" if it falls outside the subscription period.

### 7.4) Test 4 — Strict Consistency with Block Statistics

**Query file:** `TDD4_Strict_consistency_threshold_=_block_stats.sql`

**What it checks:**
The tagging in `final_dataset` must be strictly consistent with:
- the block-level statistics (`block_size`, `is_free_delivery`),
- and the threshold rule.

**Why this matters:**
This is a comprehensive test that validates the entire pipeline end-to-end. It ensures that the tagging logic correctly implements the business rule.

---

## 8) Answering the Business Question

### 8.1) How We Answer the Client's Question

**The client's need:**
The client wants to analyze how Deliveroo Plus (the loyalty program) changes customer behavior, despite the absence of explicit subscription events in historical data.

**Our solution:**
We reconstruct subscription periods using observable behavioral signals (repeated free deliveries). This enables:
- comparison of customer behavior before, during, and after subscription,
- measurement of frequency uplift and retention effects,
- analysis of churn patterns.

**How managers access the information:**
The final dataset (`final_dataset`) is designed to be immediately usable:
- Each order has a subscription flag and subscription period boundaries.
- The `subscription_phase` column allows instant segmentation.
- The `days_from_subscription_start` column enables timeline analysis.

No additional data transformation is required. The information can be directly connected to BI tools and dashboards.

### 8.2) How We Ensure the Validity of Our Approximation

**Acknowledging the approximation:**
We acknowledge that this approach is approximate by nature. However, its credibility is ensured through:

1. **Explicit business assumptions:** The rule is clearly stated, simple, and validated by the client.
2. **Behavior-based inference:** The tagging relies on the core benefit of Deliveroo Plus (free delivery), making the proxy highly aligned with the actual product mechanics.
3. **Support for multiple subscriptions:** The logic handles realistic scenarios where customers subscribe, unsubscribe, and resubscribe.
4. **Systematic validation:** Our TDD tests ensure logical coherence and temporal consistency.

**How we handle the arbitrariness of the threshold:**
The threshold is intentionally configurable. This allows:
- sensitivity analyses (testing different thresholds),
- robustness checks,
- easy alignment with evolving client requirements.

The methodology is transparent and adaptable rather than rigid.

### 8.3) Business Value for the Client

This approach enables the client to:
- quantify the impact of Deliveroo Plus on customer loyalty,
- benchmark Deliveroo's subscription strategy against competitors,
- derive actionable insights despite incomplete historical data.

By combining a clear approximation rule, scalable logic, and strong data quality checks, we provide a solution that is both pragmatic and trustworthy for decision-making.

---

## 9) Conclusion

This project demonstrates how subscription periods can be reconstructed from transactional data alone by combining:
- temporal segmentation,
- window functions,
- block-level aggregation,
- explicit business rules,
- scalable parameters,
- and systematic validation through TDD.

**Key takeaways:**
- We chose a step-by-step approach for clarity and maintainability.
- Each step builds logically on the previous one.
- The logic is transparent, explainable, and auditable.
- The output is immediately usable for business analysis.

The resulting pipeline is modular, scalable, fully SQL-based, and suitable for both analytical and managerial use cases.

---

## 10) File Structure

```
BigQuery/Querys/Queries/
├── table_creation.sql                          # Step 0
├── Step1_Subscription_block_detection.sql    # Step 1
├── Step2_block_level_aggregation.sql          # Step 2
├── Step3_Subscription_tagging.sql            # Step 3
├── Step4.1_quick_use_case_answer.sql         # Step 4.1
├── Step4.2_quick_user_case_answer.sql         # Step 4.2
├── Scalability_query.sql                      # Scalability version
├── Checking_query.sql                         # Validation queries
├── TDD1_never_subscribed_if_delivery_is_chargeable.sql
├── TDD2_if_subscribed_then_start_end_not_NULL.sql
├── TDD3_if_subscribed_datetime_in_[start, end].sql
└── TDD4_Strict_consistency_threshold_=_block_stats.sql
```

---

## 11) Usage

To execute the pipeline:

1. Run `table_creation.sql` to create `tmp_deliveroo_ordered`.
2. Run `Step1_Subscription_block_detection.sql` to create `tmp_deliveroo_blocks`.
3. Run `Step2_block_level_aggregation.sql` to create `tmp_deliveroo_block_stats`.
4. Run `Step3_Subscription_tagging.sql` to create `final_dataset`.
5. (Optional) Run `Step4.1_quick_use_case_answer.sql` and `Step4.2_quick_user_case_answer.sql` for visual enhancements.
6. Run the TDD queries to validate the logic.

To change the threshold:
- Modify the `subscription_threshold` value in `Scalability_query.sql` or in Step 3.

