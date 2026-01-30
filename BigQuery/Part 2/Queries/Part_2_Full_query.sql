/* ==================================================================================
# Taking infos from "Validated weekly" ecommerce tables to a stable delivery table. #
=================================================================================== */

DECLARE latest_table STRING;


/* Step 1)
 -> Building a clean list of weekly validated ecom tables with their creation time
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


/* Step 2)
 -> Identify the most recent validated weekly table
*/

SELECT table_name, creation_time
FROM `head-of-data-2.group_7.Part 2 --- tmp_weekly_validated_ecom_tables`
ORDER BY creation_time DESC
LIMIT 1;


/* Step 3)
 -> Copy the latest validated table into a stable output table
*/

SET latest_table = (
  SELECT table_name
  FROM `head-of-data-2.group_7.Part 2 --- tmp_weekly_validated_ecom_tables`
  ORDER BY creation_time DESC
  LIMIT 1
);

EXECUTE IMMEDIATE FORMAT("""
  CREATE OR REPLACE TABLE `head-of-data-2.group_7.last_validated_ecom` AS
  SELECT *
  FROM `head-of-data-2.assignment_data.%s`
""", latest_table);