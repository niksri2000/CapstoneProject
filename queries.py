import sqlite3
import pandas as pd

conn = sqlite3.connect('pharmeasy.db')

# 1. Row-count check comparison
print("=== 1. Row-Count Check Comparison (LEFT JOIN vs. INNER JOIN) ===")
query_left_count = """
SELECT COUNT(*) 
FROM regions_master r 
LEFT JOIN orders_clean o ON r.region = o.region;
"""
query_inner_count = """
SELECT COUNT(*) 
FROM regions_master r 
INNER JOIN orders_clean o ON r.region = o.region;
"""
left_res = pd.read_sql_query(query_left_count, conn).iloc[0, 0]
inner_res = pd.read_sql_query(query_inner_count, conn).iloc[0, 0]
print(f"LEFT JOIN Row Count: {left_res}")
print(f"INNER JOIN Row Count: {inner_res}")
print(f"Difference: {left_res - inner_res} (This represents the region with 0 orders, which is retained in LEFT JOIN but dropped in INNER JOIN)\n")

# 2. Duplicate-key check
print("=== 2. Duplicate-Key Check (Checking for non-unique order_id) ===")
query_dup = """
SELECT order_id, COUNT(*)
FROM orders_clean
GROUP BY order_id
HAVING COUNT(*) > 1;
"""
dup_df = pd.read_sql_query(query_dup, conn)
if dup_df.empty:
    print("Passed: No duplicate order_id keys found! (0 rows returned)\n")
else:
    print("Failed: Found duplicate keys:")
    display(dup_df)
    print("\n")

# 3. Null check: COUNT(*) vs COUNT(o.order_id)
print("=== 3. Null Check Pitfall: COUNT(*) vs. COUNT(fk) ===")
query_null_check = """
SELECT 
    r.region,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_fk,
    CASE WHEN COUNT(*) <> COUNT(o.order_id) THEN 'DISAGREE' ELSE 'AGREE' END AS status
FROM regions_master r
LEFT JOIN orders_clean o ON r.region = o.region
GROUP BY r.region;
"""
null_check_df = pd.read_sql_query(query_null_check, conn)
display(null_check_df)
print("Note: Kurnool (the zero-order region) returns 1 for COUNT(*) due to the null-padded row, but correctly returns 0 for COUNT(order_id).\n")

# 4. Per-region order counts
print("=== 4. Per-Region Order Counts (Ascending) ===")
query_per_region = """
SELECT 
    r.region,
    COUNT(o.order_id) AS total_orders
FROM regions_master r
LEFT JOIN orders_clean o ON r.region = o.region
GROUP BY r.region
ORDER BY total_orders ASC;
"""
per_region_df = pd.read_sql_query(query_per_region, conn)
display(per_region_df)

conn.close()


# Output
 === 1. Row-Count Check Comparison (LEFT JOIN vs. INNER JOIN) ===
LEFT JOIN Row Count: 2101
INNER JOIN Row Count: 2100
Difference: 1 (This represents the region with 0 orders, which is retained in LEFT JOIN but dropped in INNER JOIN)

=== 2. Duplicate-Key Check (Checking for non-unique order_id) ===
Passed: No duplicate order_id keys found! (0 rows returned)


