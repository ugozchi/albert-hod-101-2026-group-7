/* Most recent Validated weekly table (step 3 - Part 2)
Should identify the latest validated table we are about to ship.
*/

SELECT table_name, creation_time
FROM `head-of-data-2.group_7.Part 2 --- tmp_weekly_validated_ecom_tables`
ORDER BY creation_time DESC
LIMIT 1;
