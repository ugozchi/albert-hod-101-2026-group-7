# Ecommerce Data Consolidation: Weekly Validated Tables (SQL Only)

## File Structure

```
BigQuery/Part 2/Queries/
├── Part_2_Full_query.sql                                     # Complete pipeline
├── Step1_sanity_check_4_weekly_validated.sql                 # Step 1: Sanity check
├── Step2_Validated_weekly.sql                                # Step 2: Validated weekly tables
├── Step3_Most_recent_validated_weekly.sql                    # Step 3: Most recent table
└── Step4_safe_version_validated_weekly.sql                   # Step 4: Safe version
```

---

## 1) Project Objective

Consolidate data from **weekly validated ecommerce tables** into a stable delivery table. Work with `ecom_flat_table_*` tables marked "validated: weekly" in metadata. Identify validated tables, pick the most recent, consolidate into one stable table, ensure quality and consistency.

---

## 2) Business Context and Constraints

Ecommerce data is validated weekly; new `ecom_flat_table_*` tables are created with timestamps.

**Need:** Stable, consolidated view of the most recent validated weekly data for analysis and reporting.

**Constraint:** Multiple tables with different validation statuses; use only "validated: weekly".

**Approach:** Identify validated weekly tables → select the most recent → create stable delivery table.

---

## 3) Our Approach and Reasoning

**Methodology:** Systematic identification and validation before processing so we use correct, validated data.

**Pipeline in steps:** Same as Part 1 – readability, debuggability, maintainability, explainability.

**Order:** (1) Sanity check: list validated weekly tables → (2) Build clean list with creation times → (3) Pick most recent → (4) Create safe, stable delivery table.

---

## 4) Data Overview

**Source:** `assignment_data.ecom_flat_table_*` (labels indicate validation status).

**Intermediate (group_7):** `Part 2 --- tmp_weekly_validated_ecom_tables` (table_name, creation_time).

**Output:** Stable delivery table with consolidated validated weekly data.

---

## 5) Implementation

### Step 1) Sanity Check  
**File:** `Step1_sanity_check_4_weekly_validated.sql`  
Query `INFORMATION_SCHEMA.TABLE_OPTIONS` for `ecom_flat_table_%` with labels containing "validated" and "weekly". Result: list of validated weekly table names.

### Step 2) Build List of Validated Weekly Tables  
**File:** `Step2_Validated_weekly.sql`  
Join `INFORMATION_SCHEMA.TABLES` and `TABLE_OPTIONS`; filter validated+weekly; store table_name and creation_time in `Part 2 --- tmp_weekly_validated_ecom_tables`.

### Step 3) Most Recent Validated Weekly Table  
**File:** `Step3_Most_recent_validated_weekly.sql`  
Order tmp table by `creation_time DESC`, take first row. Result: name and creation time of latest validated weekly table.

### Step 4) Safe Version of Validated Weekly Data  
**File:** `Step4_safe_version_validated_weekly.sql`  
Create stable delivery table from the most recent table identified in Step 3. Final deliverable for analysis and reporting.

### Full Query  
**File:** `Part_2_Full_query.sql`  
Complete pipeline in one script; modular steps remain available for individual execution.

---

## 6) Data Quality and Validation

We only process tables marked "validated: weekly"; use `INFORMATION_SCHEMA` metadata; keep intermediate tables for transparency and debugging. Ensures validated, reliable data and an auditable selection process.

---

## 7) Business Value

Stable table name for consistent access; only validated weekly data; pipeline can pick latest automatically; transparent, auditable process. Reliable solution for accessing the most recent validated ecommerce data.
