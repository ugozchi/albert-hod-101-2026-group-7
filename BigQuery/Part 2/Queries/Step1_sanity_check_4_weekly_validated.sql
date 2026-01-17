/* Sanity check (step 1 - Part 2)
-> List all ecom flat tables and display their labels
 -> At the end, should identify which tables that are marked as `validated: weekly`
*/

SELECT table_name, option_name, option_value
FROM `head-of-data-2.assignment_data.INFORMATION_SCHEMA.TABLE_OPTIONS`
WHERE table_name LIKE 'ecom_flat_table_%'
  AND option_name = 'labels'
ORDER BY table_name DESC;

/* ecom_flat_table_20250427122317, ecom_flat_table_20250420050018, ecom_flat_table_20250413050012, ecom_flat_table_20250504050015 */