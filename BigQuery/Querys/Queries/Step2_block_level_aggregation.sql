/* Compute block-level stats (size + start/end datetime)
 -> Now, step 2, using metadata per block to decide if a block qualifies as a subscription.
-> We compute, for each (**customer**, **block_id**):
 -> **block_size**  = to fin the number of orders in the block
 -> **block_start** = to know first order datetime in the block
 -> **block_end**   = finally, the last order datetime in the block
*/

CREATE OR REPLACE TABLE `head-of-data-2.group_7.tmp_deliveroo_block_stats` AS
SELECT
  *,
  COUNT(*) OVER (
    PARTITION BY id_customer_synth, block_id
  ) AS block_size, -- how many orders in the same block

  MIN(order_datetime_synth) OVER (
    PARTITION BY id_customer_synth, block_id
  ) AS block_start_datetime, -- first order datetime in the block

  MAX(order_datetime_synth) OVER (
    PARTITION BY id_customer_synth, block_id
  ) AS block_end_datetime -- last order datetime in the block

FROM `head-of-data-2.group_7.tmp_deliveroo_blocks`;

/* Expected result
-> **block_size** / **block_start_datetime** / **block_end_datetime** should be constant inside a given block
*/
