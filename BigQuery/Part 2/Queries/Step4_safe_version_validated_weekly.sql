/* The last table in a validated and stable version(step 4 - Part 2)
Should copy the latest validated table into a stable output table.
*/

DECLARE latest_table STRING;

SET latest_table = (
  SELECT table_name
  FROM `head-of-data-2.group_7.Part 2 --- tmp_weekly_validated_ecom_tables`
  ORDER BY creation_time DESC
  LIMIT 1
);

EXECUTE IMMEDIATE FORMAT("""
  CREATE OR REPLACE TABLE `head-of-data-2.group_7.Part 2 --- last_validated_ecom` AS
  SELECT * FROM `head-of-data-2.assignment_data.%s`
""", latest_table);

SELECT latest_table AS shipped_table;
