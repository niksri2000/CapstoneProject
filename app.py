app_code = '''import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PharmEasy Regional Pulse", layout="wide")

st.title("💊 PharmEasy Regional Pulse Dashboard")

# --- Context-Insight-Implication (CII) Executive Summary Section ---
st.markdown("""
### 📢 Executive Summary
**Context:** Between April and June 2026, PharmEasy recorded **2,100 distinct orders** across our South Indian regional footprint, generating **Total Sales of Rupees 2,427,761.64** and **Total Profits of Rupees 363,225.43**.

**Insight:** While Hyderabad led absolute volume with 519 orders, Guntur exhibited a massive, broad-based **+122.19% Month-on-Month surge** in May (peaking at Rupees 138,738.93) before stabilizing in June, whereas Kurnool registered zero transactional activity.

**Implication:** To sustain this momentum, regional logistics and inventory levels must adapt dynamically to support Guntur\'s new Rupees 100,000.00 baseline. Please use the interactive dropdowns below to explore the detailed category breakdowns (Level 2) and the regional-monthly ledgers (Level 3) to guide your local market strategies.
""")
st.markdown("---")

# --- Database Connection ---
def load_data():
    conn = sqlite3.connect("pharmeasy.db")
    # Fetch orders joined with master to handle Kurnool (0 orders)
    query = """
    SELECT
        o.order_id,
        o.order_date,
        r.region,
        o.category,
        o.product,
        o.quantity,
        o.sales_inr,
        o.profit_inr
    FROM regions_master r
    LEFT JOIN orders_clean o ON r.region = o.region
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df_raw = load_data()

# Prepare months list
df_raw["month"] = df_raw["order_date"].str[:7]

# --- Interactive Sidebar Filter ---
st.sidebar.header("Dashboard Filters")
regions_list = sorted(list(df_raw["region"].unique()))
selected_region = st.sidebar.selectbox("Select Region Focus:", ["All Regions"] + regions_list)

# Filter Data
if selected_region == "All Regions":
    df_filtered = df_raw[df_raw["order_id"].notna()]
else:
    df_filtered = df_raw[(df_raw["region"] == selected_region) & (df_raw["order_id"].notna())]

# --- Level 1: Overview KPI Cards ---
st.subheader("Level 1: Executive Overview")
col1, col2, col3 = st.columns(3)

total_sales = df_filtered["sales_inr"].sum()
total_profit = df_filtered["profit_inr"].sum()
unique_orders = df_filtered["order_id"].nunique()

col1.metric(label="Total Sales (INR)", value=f"₹{total_sales:,.2f}")
col2.metric(label="Total Profit (INR)", value=f"₹{total_profit:,.2f}")
col3.metric(label="Distinct Order Count", value=f"{unique_orders:,}")

# --- Level 2: Category Breakdown ---
st.write("---")
st.subheader("Level 2: Category-Level Performance")
if not df_filtered.empty:
    cat_df = df_filtered.groupby("category").agg(
        sales=("sales_inr", "sum"),
        profit=("profit_inr", "sum"),
        orders=("order_id", "nunique")
    ).reset_index()

    st.markdown("#### How are sales distributed across medicinal categories?")

    # Part-of-Whole/Pie Chart (exactly 6 categories, no 3D, titled properly)
    fig_pie = px.pie(
        cat_df,
        values="sales",
        names="category",
        title="Sales Share by Category (Is OTC / Prescription Dominating?)",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    st.dataframe(cat_df.style.format({"sales": "₹{:,.2f}", "profit": "₹{:,.2f}", "orders": "{:,}"}))
else:
    st.info("No category data available for this selection.")

# --- Visualizations & Analysis ---
st.write("---")
st.subheader("Advanced Visualization & Trend Analysis")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # 1. Line/Trend Chart: Monthly Sales by Region
    # Tracing April, May, June trends.
    trend_data = df_raw[df_raw["order_id"].notna()].groupby(["region", "month"])["sales_inr"].sum().reset_index()
    # Ensure chronological sorting
    trend_data = trend_data.sort_values("month")

    # Highlight Guntur for the user
    color_map = {reg: "#7F7F7F" for reg in regions_list}
    color_map["Guntur"] = "#D62728" # Prominent crimson highlight for Guntur\'s swing

    fig_line = px.line(
        trend_data,
        x="month",
        y="sales_inr",
        color="region",
        color_discrete_map=color_map if selected_region == "All Regions" else None,
        title="How did regional sales transition MoM? (Highlighting Guntur\'s surge)",
        labels={"month": "Month (2026)", "sales_inr": "Sales Volume (INR)"}
    )
    # Enforce axis starting at 0
    fig_line.update_yaxes(range=[0, trend_data["sales_inr"].max() * 1.1])
    st.plotly_chart(fig_line, use_container_width=True)

with chart_col2:
    # 2. Comparison Bar Chart: Total Sales by Region
    bar_data = df_raw[df_raw["order_id"].notna()].groupby("region")["sales_inr"].sum().reset_index().sort_values("sales_inr", ascending=False)

    fig_bar = px.bar(
        bar_data,
        x="region",
        y="sales_inr",
        title="Which regions are driving our overall sales volume?",
        labels={"region": "Region Name", "sales_inr": "Total Sales (INR)"},
        color_discrete_sequence=["#1F77B4"]
    )
    # Enforce axis starting at 0
    fig_bar.update_yaxes(range=[0, bar_data["sales_inr"].max() * 1.1])
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Level 3: Regional-Monthly Detail Table ---
st.write("---")
st.subheader("Level 3: Granular Regional/Monthly Ledger")

detail_query = """
SELECT
    r.region,
    SUBSTR(o.order_date, 1, 7) AS order_month,
    SUM(o.sales_inr) AS monthly_sales,
    SUM(o.profit_inr) AS monthly_profit,
    COUNT(DISTINCT o.order_id) AS monthly_orders
FROM regions_master r
LEFT JOIN orders_clean o ON r.region = o.region
GROUP BY r.region, order_month
ORDER BY r.region, order_month;
"""
conn = sqlite3.connect("pharmeasy.db")
df_detail = pd.read_sql_query(detail_query, conn)
conn.close()

# Fill zero-order regions representation
df_detail["monthly_sales"] = df_detail["monthly_sales"].fillna(0.0)
df_detail["monthly_profit"] = df_detail["monthly_profit"].fillna(0.0)
df_detail["monthly_orders"] = df_detail["monthly_orders"].fillna(0)

if selected_region != "All Regions":
    df_detail = df_detail[df_detail["region"] == selected_region]

st.dataframe(
    df_detail.style.format({
        "monthly_sales": "₹{:,.2f}",
        "monthly_profit": "₹{:,.2f}",
        "monthly_orders": "{:,}"
    })
)
'''