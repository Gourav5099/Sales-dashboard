"""
Sales & Business Performance Analysis Dashboard
Built with Streamlit & Plotly
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Sales & Business Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1F4E79;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #555555;
        margin-bottom: 1.5rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1F4E79;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        color: #666666;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# 2. Data Loading & Caching
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_candidates = [
        os.path.join(base_dir, "sales_data_cleaning.csv"),
        os.path.join(base_dir, "excel", "sales_data_cleaning.xlsx.csv"),
        os.path.join(base_dir, "data", "sales_data_cleaning.csv"),
    ]
    file_path = None
    for p in csv_candidates:
        if os.path.exists(p):
            file_path = p
            break

    if not file_path:
        st.error("Dataset 'sales_data_cleaning.csv' not found. Please verify the file path.")
        st.stop()

    df = pd.read_csv(file_path)

    # Standardize column types
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(1).astype(int)
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce").fillna(0.0)
    df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce").fillna(0.0)
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce").fillna(0.0)

    # Canonical Category mapping
    prod_to_cat = {
        "Laptop Stand": "Technology", "External SSD 1TB": "Technology", "Dual Monitor Arm": "Technology",
        "USB-C Docking Station": "Technology", "Mechanical Keyboard": "Technology", "HD Webcam 1080p": "Technology",
        "Noise-Canceling Headset": "Technology",
        "Ergonomic Office Chair": "Furniture", "Standing Desk Converter": "Furniture", "Bookshelf 4-Tier": "Furniture",
        "Filing Cabinet": "Furniture", "Desk Organizer Mesh": "Furniture", "Adjustable Footrest": "Furniture",
        "Lumbar Support Cushion": "Furniture",
        "Heavy-Duty Stapler": "Office Supplies", "A4 Printer Paper (Ream)": "Office Supplies",
        "Ballpoint Pens (Pack of 12)": "Office Supplies", "Whiteboard Markers": "Office Supplies",
        "Permanent Sticky Notes": "Office Supplies", "Spiral Notebooks (3-Pack)": "Office Supplies",
        "Document Folder Set": "Office Supplies",
        "Bluetooth Speaker": "Electronics", "Surge Protector Power Strip": "Electronics",
        "Wireless Charging Pad": "Electronics", "HDMI Cable 4K (6ft)": "Electronics",
        "Portable Power Bank 20000mAh": "Electronics", "Wireless Laser Presenter": "Electronics"
    }
    df["Category"] = df["Product"].map(prod_to_cat).fillna(df["Category"])

    # Standardize Region
    reg_clean = df["Region"].fillna("").astype(str).str.strip().str.capitalize()
    df["Region"] = reg_clean.replace({"": "East", "East ": "East", "North ": "North", "South ": "South", "West ": "West"})

    df["YearMonth"] = df["Order_Date"].dt.to_period("M").astype(str)
    return df

df_raw = load_data()


# 3. Sidebar Interactive Filters
st.sidebar.image("https://img.icons8.com/fluency/96/combo-chart.png", width=64)
st.sidebar.title("Dashboard Filters")
st.sidebar.markdown("Refine your analytics view below:")

# Date Range Filter
min_date = df_raw["Order_Date"].min().date()
max_date = df_raw["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Region Filter
available_regions = sorted(df_raw["Region"].unique())
selected_regions = st.sidebar.multiselect(
    "Select Sales Region(s)",
    options=available_regions,
    default=available_regions
)

# Category Filter
available_categories = sorted(df_raw["Category"].unique())
selected_categories = st.sidebar.multiselect(
    "Select Product Category(ies)",
    options=available_categories,
    default=available_categories
)

# Filter Data
if len(date_range) == 2:
    start_dt, end_dt = date_range
    mask = (
        (df_raw["Order_Date"].dt.date >= start_dt) &
        (df_raw["Order_Date"].dt.date <= end_dt) &
        (df_raw["Region"].isin(selected_regions)) &
        (df_raw["Category"].isin(selected_categories))
    )
else:
    mask = (
        (df_raw["Region"].isin(selected_regions)) &
        (df_raw["Category"].isin(selected_categories))
    )

filtered_df = df_raw[mask].copy()

# Sidebar Metadata
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Records Displayed**: {len(filtered_df):,} of {len(df_raw):,}")
st.sidebar.caption("Sales & Business Performance Analysis • College Project")


# 4. Header Section
st.markdown("<div class='main-title'>📊 Sales & Business Performance Executive Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Interactive Business Intelligence overview evaluating Revenue, Margins, Categories, and Regional Performance.</div>", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("⚠️ No records match your selected filters. Please adjust the sidebar filter options.")
    st.stop()


# 5. Top KPI Scorecards
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0.0
total_orders = filtered_df["Order_ID"].nunique()
avg_order_val = (total_sales / total_orders) if total_orders > 0 else 0.0
total_units = filtered_df["Quantity"].sum()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Revenue", f"${total_sales:,.2f}")
col2.metric("Net Profit", f"${total_profit:,.2f}")
col3.metric("Profit Margin", f"{profit_margin:.2f}%")
col4.metric("Total Orders", f"{total_orders:,}")
col5.metric("Avg Order Value", f"${avg_order_val:,.2f}")

st.markdown("---")


# 6. Row 1: Sales Trend & Category Share
chart_col1, chart_col2 = st.columns([6, 4])

with chart_col1:
    st.subheader("📈 Monthly Sales & Profit Trend")
    trend_df = filtered_df.groupby("YearMonth").agg(
        Monthly_Sales=("Sales", "sum"),
        Monthly_Profit=("Profit", "sum")
    ).reset_index().sort_values("YearMonth")

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=trend_df["YearMonth"],
        y=trend_df["Monthly_Sales"],
        mode="lines+markers",
        name="Gross Sales ($)",
        line=dict(color="#1F4E79", width=3),
        marker=dict(size=6)
    ))
    fig_trend.add_trace(go.Scatter(
        x=trend_df["YearMonth"],
        y=trend_df["Monthly_Profit"],
        mode="lines+markers",
        name="Net Profit ($)",
        line=dict(color="#2CA02C", width=2.5, dash="dash"),
        marker=dict(size=6),
        fill="tozeroy",
        fillcolor="rgba(44, 160, 44, 0.08)"
    ))
    fig_trend.update_layout(
        xaxis_title="Trading Month",
        yaxis_title="Amount ($)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=30, b=20),
        height=380,
        plot_bgcolor="#FAFAFA"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with chart_col2:
    st.subheader("🍩 Category Revenue Share")
    cat_df = filtered_df.groupby("Category").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    ).reset_index().sort_values("Total_Sales", ascending=False)
    cat_df["Margin"] = (cat_df["Total_Profit"] / cat_df["Total_Sales"] * 100).round(1)

    fig_donut = px.pie(
        cat_df,
        values="Total_Sales",
        names="Category",
        hole=0.5,
        color_discrete_sequence=["#1F4E79", "#2E75B6", "#5DADE2", "#A9CCE3"],
        hover_data={"Total_Sales": ":$,.2f", "Margin": True}
    )
    fig_donut.update_traces(
        textposition="outside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Sales: %{value:$,.2f}<br>Share: %{percent}<br>Margin: %{customdata[0]:.1f}%"
    )
    fig_donut.update_layout(
        annotations=[dict(text=f"<b>${total_sales*1e-3:.0f}K</b><br>Total", x=0.5, y=0.5, font_size=15, showarrow=False)],
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=20),
        height=380
    )
    st.plotly_chart(fig_donut, use_container_width=True)


# 7. Row 2: Top Products & Regional Comparison
chart_col3, chart_col4 = st.columns([5, 5])

with chart_col3:
    st.subheader("🏆 Top 5 Revenue-Generating Products")
    top_prod = filtered_df.groupby(["Product", "Category"]).agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum")
    ).reset_index().sort_values("Total_Sales", ascending=True).tail(5)

    top_prod["Margin"] = (top_prod["Total_Profit"] / top_prod["Total_Sales"] * 100).round(1)

    fig_prod = px.bar(
        top_prod,
        x="Total_Sales",
        y="Product",
        orientation="h",
        text_auto="$,.0f",
        color="Total_Sales",
        color_continuous_scale="Blues",
        hover_data={"Total_Sales": ":$,.2f", "Total_Profit": ":$,.2f", "Units_Sold": True, "Margin": True}
    )
    fig_prod.update_traces(textposition="outside", cliponaxis=False)
    fig_prod.update_layout(
        xaxis_title="Sales ($)",
        yaxis_title="",
        coloraxis_showscale=False,
        margin=dict(l=20, r=40, t=30, b=20),
        height=360,
        plot_bgcolor="#FAFAFA"
    )
    st.plotly_chart(fig_prod, use_container_width=True)

with chart_col4:
    st.subheader("🗺️ Regional Sales vs. Net Profit")
    reg_df = filtered_df.groupby("Region").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    ).reset_index().sort_values("Total_Sales", ascending=False)

    fig_reg = go.Figure()
    fig_reg.add_trace(go.Bar(
        x=reg_df["Region"],
        y=reg_df["Total_Sales"],
        name="Gross Sales ($)",
        marker_color="#1F4E79",
        text=reg_df["Total_Sales"].apply(lambda x: f"${x*1e-3:.1f}K"),
        textposition="outside"
    ))
    fig_reg.add_trace(go.Bar(
        x=reg_df["Region"],
        y=reg_df["Total_Profit"],
        name="Net Profit ($)",
        marker_color="#2CA02C",
        text=reg_df["Total_Profit"].apply(lambda x: f"${x*1e-3:.1f}K"),
        textposition="outside"
    ))
    fig_reg.update_layout(
        barmode="group",
        yaxis_title="Amount ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=30, b=20),
        height=360,
        plot_bgcolor="#FAFAFA"
    )
    st.plotly_chart(fig_reg, use_container_width=True)

# 8. Interactive Data Table View
st.markdown("---")
with st.expander("🔍 View & Search Filtered Transaction Records"):
    st.dataframe(
        filtered_df[[
            "Order_ID", "Order_Date", "Customer_ID", "Product", "Category",
            "Region", "Quantity", "Sales", "Discount", "Profit"
        ]],
        use_container_width=True,
        hide_index=True
    )
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )
