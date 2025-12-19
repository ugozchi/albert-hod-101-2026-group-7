/* TDD - Test 1
-> is_free_delivery = 0 cannot be tagged as subscription
-> Expected: 0
*/
SELECT COUNT(*) AS should_be_zero
FROM `head-of-data-2.group_7.final_dataset`
WHERE is_free_delivery = 0
  AND is_order_made_during_subscription = 1;
