/* Build "blocks" of consecutive orders per customer
-> trying to detect multiple subscription periods by customer.
 -> To do that, we split each customer's timeline into consecutive blocks ("blocks")
 -> where **is_free_delivery** stays the same (binary 1 or 0).
 -> A new block starts when **is_free_delivery** changes compared to the previous order
*/

CREATE OR REPLACE TABLE `head-of-data-2.group_7.tmp_deliveroo_blocks` AS
SELECT
  *,
  SUM(
    CASE
      WHEN prev_is_free_delivery IS NULL THEN 1
      WHEN is_free_delivery != prev_is_free_delivery THEN 1 -- if there is a change, we start a new block
      ELSE 0
    END
  ) OVER (
    PARTITION BY id_customer_synth -- independant block per customer
    ORDER BY order_datetime_synth
  ) AS block_id
FROM `head-of-data-2.group_7.tmp_deliveroo_ordered`;

/* Expected result
-> **block_id** ===> For a given customer, block_id will look like 1,1,1,2,2,3,3...
 -> each "free delivery block" is a separate candidate subscription period. 
 */