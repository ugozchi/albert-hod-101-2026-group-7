/* Final deliverable table
-> test
*/

CREATE OR REPLACE TABLE `head-of-data-2.group_7.enriched_synthetic_deliveroo_plus_dataset_test` AS
SELECT
  id_customer_synth,
  order_datetime_synth,
  is_free_delivery,

  IF(is_free_delivery = 1 AND block_size >= 3, 1, 0) AS is_order_made_during_subscription,

  IF(is_free_delivery = 1 AND block_size >= 3, block_start_datetime, NULL)
    AS current_subscription_start_datetime,

  IF(is_free_delivery = 1 AND block_size >= 3, block_end_datetime, NULL)
    AS current_subscription_end_datetime

FROM `head-of-data-2.group_7.tmp_deliveroo_block_stats`;

/* Expected result
*/