/* Visual enhancement
-> Add a phase label per order: BEFORE / DURING / AFTER subscription.
*/

CREATE OR REPLACE TABLE `head-of-data-2.group_7.final_dataset_final1` AS
WITH base AS (
  SELECT
    f.*,

    -- For each customer, the next subscription start after this order (if any)
    MIN(current_subscription_start_datetime) OVER (
      PARTITION BY id_customer_synth
      ORDER BY order_datetime_synth
      ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
    ) AS next_sub_start,

    -- For each customer, the last subscription end before this order (if any)
    MAX(current_subscription_end_datetime) OVER (
      PARTITION BY id_customer_synth
      ORDER BY order_datetime_synth
      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS prev_sub_end
  FROM `head-of-data-2.group_7.final_dataset` f
)
SELECT
  *,
  CASE
    WHEN is_order_made_during_subscription = 1 THEN 'DURING'
    WHEN next_sub_start IS NOT NULL AND order_datetime_synth < next_sub_start THEN 'BEFORE'
    WHEN prev_sub_end IS NOT NULL AND order_datetime_synth > prev_sub_end THEN 'AFTER'
    ELSE 'NO_SUBSCRIPTION_INFO'
  END AS subscription_phase
FROM base;
