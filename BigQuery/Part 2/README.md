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

The objective of this project is to consolidate data from **weekly validated ecommerce tables** into a stable delivery table. We work with multiple `ecom_flat_table_*` tables that are marked as "validated: weekly" in their metadata.

The core challenge is to:
- Identify which tables are validated weekly
- Extract the most recent validated weekly table
- Consolidate the data into a stable, reliable delivery table
- Ensure data quality and consistency

---

## 2) Business Context and Constraints

Ecommerce data is collected and validated on a weekly basis, creating new `ecom_flat_table_*` tables with timestamps. Each table contains validated ecommerce transaction data.

**The business need:** Create a stable, consolidated view of the most recent validated weekly data that can be used for analysis and reporting.

**The constraint:** Multiple tables exist with different validation statuses. We need to identify and use only the "validated: weekly" tables.

**The approach:** We systematically identify validated weekly tables, select the most recent one, and create a stable delivery table from it.

---

## 3) Our Approach and Reasoning

### 3.1) Why We Chose This Methodology

We decided to use a systematic approach to identify and validate tables before processing. This ensures we work with the correct, validated data rather than potentially incomplete or unvalidated tables.

### 3.2) Why We Structured the Pipeline in Steps

We chose to break down the problem into explicit, sequential steps for the same reasons as Part 1:

- **Readability:** Each step has a single, clear responsibility
- **Debuggability:** We can validate each intermediate result
- **Maintainability:** Future modifications are easier when the logic is modular
- **Explainability:** We can explain our reasoning step by step

### 3.3) Why This Order of Steps

The order of steps follows a logical progression:

1. **First**, we identify all validated weekly tables (Step 1: Sanity check)
2. **Then**, we build a clean list of validated weekly tables (Step 2)
3. **Next**, we identify the most recent validated weekly table (Step 3)
4. **Finally**, we create a safe, stable version of the consolidated data (Step 4)

---

## 4) Data Overview

### 4.1) Source Dataset
- `assignment_data.ecom_flat_table_*`: Multiple ecommerce flat tables with timestamps
- Tables are marked with labels indicating validation status

### 4.2) Intermediate Tables (created in `group_7`)
- `Part 2 --- tmp_weekly_validated_ecom_tables`: List of validated weekly tables

### 4.3) Output Tables
- Stable delivery table with consolidated validated weekly data

---

## 5) Implementation

### Step 1) Sanity Check: Identify Validated Weekly Tables

**Query file:** `Step1_sanity_check_4_weekly_validated.sql`

**What we do:**
We query the `INFORMATION_SCHEMA.TABLE_OPTIONS` to identify all `ecom_flat_table_*` tables that have labels containing "validated" and "weekly".

**Why this step is necessary:**
Before processing, we need to verify which tables are available and which ones are marked as validated weekly. This sanity check ensures we're working with the correct set of tables.

**How it works:**
- We query `INFORMATION_SCHEMA.TABLE_OPTIONS` for tables matching the pattern `ecom_flat_table_%`
- We filter for tables with labels containing "validated" and "weekly"
- We display the table names and their labels

**Expected result:**
A list of table names that are marked as validated weekly (e.g., `ecom_flat_table_20250427122317`, `ecom_flat_table_20250420050018`, etc.).

---

### Step 2) Build List of Validated Weekly Tables

**Query file:** `Step2_Validated_weekly.sql`

**What we do:**
We create a temporary table containing all validated weekly ecommerce tables with their creation times.

**Why this step is crucial:**
We need a clean, structured list of validated tables with their metadata (especially creation time) to identify the most recent one.

**How it works:**
- We join `INFORMATION_SCHEMA.TABLES` with `INFORMATION_SCHEMA.TABLE_OPTIONS`
- We filter for tables with labels containing "validated" and "weekly"
- We store the table names and creation times in a temporary table

**Expected result:**
A temporary table `Part 2 --- tmp_weekly_validated_ecom_tables` with columns:
- `table_name`: Name of the validated weekly table
- `creation_time`: When the table was created

---

### Step 3) Identify Most Recent Validated Weekly Table

**Query file:** `Step3_Most_recent_validated_weekly.sql`

**What we do:**
We identify the most recent validated weekly table by ordering the temporary table by creation time and selecting the latest one.

**Why this step is essential:**
We want to work with the most up-to-date validated data. This step ensures we select the latest validated weekly table.

**How it works:**
- We query the temporary table created in Step 2
- We order by `creation_time DESC`
- We select the first row (most recent)

**Expected result:**
The name and creation time of the most recent validated weekly table.

---

### Step 4) Create Safe Version of Validated Weekly Data

**Query file:** `Step4_safe_version_validated_weekly.sql`

**What we do:**
We create a stable, safe version of the consolidated data from the most recent validated weekly table.

**Why this step is important:**
This creates the final deliverable - a stable table that can be used for analysis and reporting without worrying about table names changing.

**How it works:**
- We use the most recent validated weekly table identified in Step 3
- We create a stable delivery table with the consolidated data
- The table structure and data are preserved from the source

**Expected result:**
A stable delivery table containing the consolidated validated weekly ecommerce data.

---

### Full Query: Complete Pipeline

**Query file:** `Part_2_Full_query.sql`

**What we do:**
This file contains the complete pipeline combining all steps into a single script.

**Why we have this:**
It provides a convenient way to run the entire process in one go, while still maintaining the modular structure for individual step execution.

---

## 6) Data Quality and Validation

**Our validation approach:**
- We only process tables explicitly marked as "validated: weekly"
- We use metadata from `INFORMATION_SCHEMA` to ensure data quality
- We create intermediate tables for transparency and debugging

**Why this matters:**
- Ensures we work with validated, reliable data
- Prevents processing of incomplete or unvalidated tables
- Makes the data selection process transparent and auditable

---

## 7) Business Value

This approach enables:
- **Consistent data access:** A stable table that doesn't change name
- **Data quality assurance:** Only validated weekly tables are used
- **Automated updates:** The pipeline can identify and use the latest validated data
- **Transparency:** Clear process for identifying and selecting validated tables

By combining systematic table identification, validation checks, and stable table creation, we provide a reliable solution for accessing the most recent validated ecommerce data.
