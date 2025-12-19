/* TDD - Test 4
-> tagging in final_dataset must match the rule applied on block_stats
-> Expected: 0
*/
SELECT COUNT(*) AS should_be_zero
FROM `head-of-data-2.group_7.tmp_deliveroo_block_stats` s
JOIN `head-of-data-2.group_7.final_dataset` f
  ON f.id_customer_synth = s.id_customer_synth
 AND f.order_datetime_synth = s.order_datetime_synth
 AND f.is_free_delivery = s.is_free_delivery
CROSS JOIN (
  SELECT 3 AS subscription_threshold
) p
WHERE
  (
    s.is_free_delivery = 1 AND s.block_size >= p.subscription_threshold
    AND f.is_order_made_during_subscription != 1
  )
  OR
  (
    NOT (s.is_free_delivery = 1 AND s.block_size >= p.subscription_threshold)
    AND f.is_order_made_during_subscription != 0
  );