/* Validated weekly list & creation_time (step 2 - Part 2)
Should build a clean list of weekly validated ecom tables with their creation time.
*/

CREATE OR REPLACE TABLE `head-of-data-2.group_7.Part 2 --- tmp_weekly_validated_ecom_tables` AS
SELECT t.table_name, t.creation_time
FROM `head-of-data-2.assignment_data.INFORMATION_SCHEMA.TABLES` t
JOIN `head-of-data-2.assignment_data.INFORMATION_SCHEMA.TABLE_OPTIONS` o
  ON t.table_name = o.table_name
WHERE t.table_name LIKE 'ecom_flat_table_%'
  AND o.option_name = 'labels'
  AND LOWER(o.option_value) LIKE '%validated%'
  AND LOWER(o.option_value) LIKE '%weekly%';
