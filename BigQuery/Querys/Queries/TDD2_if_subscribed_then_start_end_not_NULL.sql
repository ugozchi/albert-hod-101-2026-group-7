/* TDD - Test 2
-> subscribed orders must have start/end filled
-> Expected: 0
*/
SELECT COUNT(*) AS should_be_zero
FROM `head-of-data-2.group_7.final_dataset`
WHERE is_order_made_during_subscription = 1
  AND (current_subscription_start_datetime IS NULL
       OR current_subscription_end_datetime IS NULL);