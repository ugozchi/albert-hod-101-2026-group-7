/* TDD - Test 3
-> subscribed orders must be within subscription time window
-> Expected: 0
*/
SELECT COUNT(*) AS should_be_zero
FROM `head-of-data-2.group_7.final_dataset`
WHERE is_order_made_during_subscription = 1
  AND NOT (
    order_datetime_synth >= current_subscription_start_datetime
    AND order_datetime_synth <= current_subscription_end_datetime
  );