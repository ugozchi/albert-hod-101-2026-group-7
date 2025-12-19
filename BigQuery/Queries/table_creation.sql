CREATE OR REPLACE TABLE `head-of-data-2.group_7.tmp_deliveroo_ordered` AS
SELECT
  id_customer_synth,
  order_datetime_synth,
  is_free_delivery,
  LAG(is_free_delivery) OVER (
    PARTITION BY id_customer_synth
    ORDER BY order_datetime_synth
  ) AS prev_is_free_delivery
FROM `head-of-data-2.assignment_data.synthetic_deliveroo_plus_dataset`;
