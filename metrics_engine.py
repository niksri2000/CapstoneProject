import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('pharmeasy.db')

# SQL query to extract sales per region and month
query = """
SELECT 
    r.region,
    SUBSTR(o.order_date, 1, 7) AS order_month,
    SUM(o.sales_inr) AS total_sales
FROM regions_master r
LEFT JOIN orders_clean o ON r.region = o.region
GROUP BY r.region, order_month
ORDER BY r.region, order_month;
"""

# Load into a pandas DataFrame
df_monthly = pd.read_sql_query(query, conn)

# Pivot to have months as columns
df_pivot = df_monthly.pivot(index='region', columns='order_month', values='total_sales').fillna(0)

# Drop column associated with None (the zero-order region with no matching dates)
if None in df_pivot.columns:
    df_pivot = df_pivot.drop(columns=[None])

# Ensure columns for April, May, and June exist
months = ['2026-04', '2026-05', '2026-06']
for m in months:
    if m not in df_pivot.columns:
        df_pivot[m] = 0.0

# Calculate Month-on-Month (MoM) growth percentages
# Formula: (Current - Previous) / Previous * 100
df_pivot['MoM_Apr_to_May_Pct'] = ((df_pivot['2026-05'] - df_pivot['2026-04']) / df_pivot['2026-04'] * 100).round(2)
df_pivot['MoM_May_to_Jun_Pct'] = ((df_pivot['2026-06'] - df_pivot['2026-05']) / df_pivot['2026-05'] * 100).round(2)

# Format the columns for visualization
df_display = df_pivot[['2026-04', '2026-05', '2026-06', 'MoM_Apr_to_May_Pct', 'MoM_May_to_Jun_Pct']].copy()
df_display.columns = ['April Sales (INR)', 'May Sales (INR)', 'June Sales (INR)', 'Apr -> May Growth %', 'May -> Jun Growth %']

# Display the table
display(df_display)

conn.close()


# Significance flagging with state persistence

import json
import os

def compute_percentage_change_v1(current, previous):
    if previous == 0:
        return 0.0
    return round(((current - previous) / previous) * 100, 2)

def flag_significant_regions_v1(changes, threshold=8):
    flags = {}
    for region, change in changes.items():
        flags[region] = abs(change) > threshold
    return flags

def save_state_v1(month_summary, path):
    with open(path, 'w') as f:
        json.dump(month_summary, f, indent=4)
    print(f"Saved month summary to {path}")

def load_previous_state_v1(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return json.load(f)

# Let's extract values and demonstrate
apr_sales = df_display['April Sales (INR)'].to_dict()
may_sales = df_display['May Sales (INR)'].to_dict()
june_sales = df_display['June Sales (INR)'].to_dict()

# Calculate April -> May changes using compute_percentage_change_v1
ap_may_changes = {reg: compute_percentage_change_v1(may_sales[reg], apr_sales[reg]) for reg in apr_sales}

# Flag significant changes for Apr -> May
ap_may_flags = flag_significant_regions_v1(ap_may_changes, threshold=8)

# Build a monthly summary dictionary
month_summary = {
    "month": "2026-05",
    "sales": may_sales,
    "previous_sales": apr_sales,
    "changes": ap_may_changes,
    "significant_flags": ap_may_flags
}

# Demonstrate state persistence
state_file = 'month_summary_state.json'
save_state_v1(month_summary, state_file)

loaded_summary = load_previous_state_v1(state_file)
print("\n--- Loaded State Summary ---")
print(json.dumps(loaded_summary, indent=2))

# Saved month summary to month_summary_state.json

--- Loaded State Summary ---
{
  "month": "2026-05",
  "sales": {
    "Bengaluru": 172929.68,
    "Guntur": 138738.93,
    "Hyderabad": 243825.28,
    "Karimnagar": 61585.9,
    "Kurnool": 0.0,
    "Nellore": 91184.86,
    "Tirupati": 91083.2,
    "Vijayawada": 174863.57,
    "Visakhapatnam": 50590.08,
    "Warangal": 78339.23
  },
  "previous_sales": {
    "Bengaluru": 203505.48,
    "Guntur": 62442.270000000004,
    "Hyderabad": 209670.15,
    "Karimnagar": 49815.71,
    "Kurnool": 0.0,
    "Nellore": 85623.19,
    "Tirupati": 54582.74,
    "Vijayawada": 171334.19,
    "Visakhapatnam": 134765.29,
    "Warangal": 100468.14
  },
  "changes": {
    "Bengaluru": -15.02,
    "Guntur": 122.19,
    "Hyderabad": 16.29,
    "Karimnagar": 23.63,
    "Kurnool": 0.0,
    "Nellore": 6.5,
    "Tirupati": 66.87,
    "Vijayawada": 2.06,
    "Visakhapatnam": -62.46,
    "Warangal": -22.03
  },
  "significant_flags": {
    "Bengaluru": true,
    "Guntur": true,
    "Hyderabad": true,
    "Karimnagar": true,
    "Kurnool": false,
    "Nellore": false,
    "Tirupati": true,
    "Vijayawada": false,
    "Visakhapatnam": true,
    "Warangal": true
  }
}