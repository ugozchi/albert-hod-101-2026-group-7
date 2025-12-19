/* Scalability
-> Subscription threshold defined once.
 -> Changing 3 -> 20 updates the whole logic.
*/

CREATE OR REPLACE TABLE `head-of-data-2.group_7.Scalability_dataset` AS
SELECT
  s.id_customer_synth,
  s.order_datetime_synth,
  s.is_free_delivery,

  IF(
    s.is_free_delivery = 1
    AND s.block_size >= p.subscription_threshold,
    1,
    0
  ) AS is_order_made_during_subscription,

  IF(
    s.is_free_delivery = 1
    AND s.block_size >= p.subscription_threshold,
    s.block_start_datetime,
    NULL
  ) AS current_subscription_start_datetime,

  IF(
    s.is_free_delivery = 1
    AND s.block_size >= p.subscription_threshold,
    s.block_end_datetime,
    NULL
  ) AS current_subscription_end_datetime

FROM `head-of-data-2.group_7.tmp_deliveroo_block_stats` s
CROSS JOIN (
  SELECT 3 AS subscription_threshold
) p;

/* Expected result
-> Only one value to change : **subscription_threshold**.
 -> Example: set it to 20 to require 20 consecutive free deliveries.
*/