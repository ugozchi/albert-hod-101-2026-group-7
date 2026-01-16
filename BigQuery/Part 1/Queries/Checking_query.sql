/* Check client
--> 2888
*/

SELECT
  id_customer_synth,
  order_datetime_synth,
  is_free_delivery,
  is_order_made_during_subscription,
  current_subscription_start_datetime,
  current_subscription_end_datetime
FROM `head-of-data-2.group_7.final_dataset`
WHERE id_customer_synth = 2888
ORDER BY order_datetime_synth;
