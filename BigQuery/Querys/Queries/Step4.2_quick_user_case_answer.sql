/* Visual enhancement
-> Add a relative day index inside subscription periods.
*/

CREATE OR REPLACE TABLE `head-of-data-2.group_7.final_dataset_final2` AS
SELECT
  f.*,

  IF(
    f.is_order_made_during_subscription = 1,
    DATE_DIFF(
      DATE(f.order_datetime_synth),
      DATE(f.current_subscription_start_datetime),
      DAY
    ),
    NULL
  ) AS days_from_subscription_start

FROM `head-of-data-2.group_7.final_dataset_final1` f;
