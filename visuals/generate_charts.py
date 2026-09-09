"""
Generate Executive Dashboard Visualizations
Project: Sales & Business Performance Analysis
Tools: Python, Matplotlib, Pandas, SQLite

Charts Generated:
1. visuals/01_sales_trend.png          - Monthly Sales & Profit Trend (Line Chart)
2. visuals/02_top_5_products.png        - Top 5 Products by Revenue (Horizontal Bar Chart)
3. visuals/03_category_sales_donut.png  - Category Revenue Share & Profitability (Donut Chart)
4. visuals/04_regional_performance.png  - Regional Sales & Margin Comparison (Clustered Bar Chart)
"""

import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Setup paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "sql", "sales_analysis.db")
OUTPUT_DIR = CURRENT_DIR

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set global visual styling
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Segoe UI", "Arial", "DejaVu Sans"]
plt.rcParams["axes.edgecolor"] = "#CCCCCC"
plt.rcParams["axes.linewidth"] = 0.8


def load_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT 
        Order_ID,
        Order_Date,
        Customer_ID,
        Product,
        Category,
        Region,
        Quantity,
        Sales,
        Discount,
        Profit
    FROM sales_data;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Canonical product to category mapping
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

    # Standardize region
    reg_clean = df["Region"].fillna("").astype(str).str.strip().str.capitalize()
    df["Region"] = reg_clean.replace({"": "East", "East ": "East", "North ": "North", "South ": "South", "West ": "West"})

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["YearMonth"] = df["Order_Date"].dt.to_period("M").astype(str)
    return df


def plot_sales_trend(df):
    """Chart 1: Total Sales & Profit Trend Over Time (Line Chart)"""
    monthly = df.groupby("YearMonth").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    ).reset_index()

    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)

    # Plot lines
    ax.plot(monthly["YearMonth"], monthly["Total_Sales"], marker="o", color="#1F4E79",
            linewidth=2.5, markersize=5, label="Total Sales ($)")
    ax.plot(monthly["YearMonth"], monthly["Total_Profit"], marker="s", color="#2CA02C",
            linewidth=2.2, markersize=5, linestyle="--", label="Net Profit ($)")

    # Fill area under profit line
    ax.fill_between(monthly["YearMonth"], monthly["Total_Profit"], color="#2CA02C", alpha=0.1)

    # Title & Labels
    ax.set_title("Monthly Sales & Profit Performance Trend (2023 - 2024)",
                 fontsize=14, fontweight="bold", pad=20, color="#1F4E79")
    ax.set_xlabel("Trading Month (Year-Month)", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("Amount in USD ($)", fontsize=11, fontweight="bold", labelpad=10)

    # Format y-axis as currency and set headroom
    formatter = ticker.FuncFormatter(lambda x, pos: f"${x * 1e-3:.0f}K")
    ax.yaxis.set_major_formatter(formatter)
    ax.set_ylim(0, max(monthly["Total_Sales"]) * 1.24)

    # X-axis ticks
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.yticks(fontsize=10)
    ax.grid(True, linestyle=":", alpha=0.6)

    # Highlight peak month
    peak_idx = monthly["Total_Sales"].idxmax()
    peak_month = monthly.loc[peak_idx, "YearMonth"]
    peak_sales = monthly.loc[peak_idx, "Total_Sales"]
    ax.annotate(f"Peak Month: {peak_month}\n${peak_sales:,.0f}",
                xy=(peak_idx, peak_sales),
                xytext=(peak_idx - 3, peak_sales + 2200),
                arrowprops=dict(facecolor="#D9534F", edgecolor="#D9534F", arrowstyle="->", lw=1.5),
                fontsize=9, fontweight="bold", color="#A93226",
                bbox=dict(boxstyle="round,pad=0.3", fc="#FDEDEC", ec="#D9534F", lw=1))

    ax.legend(loc="upper left", frameon=True, fontsize=10)
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, "01_sales_trend.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Saved: {out_path}")


def plot_top_5_products(df):
    """Chart 2: Top 5 Products by Sales (Horizontal Bar Chart)"""
    top5 = df.groupby(["Product", "Category"]).agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum")
    ).reset_index().sort_values("Total_Sales", ascending=True).tail(5)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    # Palette
    colors = ["#5DADE2", "#48C9B0", "#F5B041", "#5499C7", "#1F4E79"]
    bars = ax.barh(top5["Product"], top5["Total_Sales"], color=colors, height=0.6, edgecolor="#333333", lw=0.6)

    ax.set_title("Top 5 Revenue-Generating Products", fontsize=14, fontweight="bold", pad=15, color="#1F4E79")
    ax.set_xlabel("Total Sales in USD ($)", fontsize=11, fontweight="bold", labelpad=10)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"${x * 1e-3:.0f}K"))

    # Add data labels
    for bar, (_, row) in zip(bars, top5.iterrows()):
        width = bar.get_width()
        margin = (row["Total_Profit"] / row["Total_Sales"]) * 100
        ax.text(width + 1000, bar.get_y() + bar.get_height() / 2,
                f"${width:,.0f}  (Margin: {margin:.1f}%)",
                va="center", ha="left", fontsize=9.5, fontweight="bold", color="#2C3E50")

    ax.set_xlim(0, max(top5["Total_Sales"]) * 1.25)
    plt.yticks(fontsize=10, fontweight="bold")
    plt.xticks(fontsize=10)
    ax.grid(axis="x", linestyle=":", alpha=0.6)
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, "02_top_5_products.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Saved: {out_path}")


def plot_category_donut(df):
    """Chart 3: Category-Wise Sales Share (Donut Chart)"""
    cat_summary = df.groupby("Category").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    ).reset_index().sort_values("Total_Sales", ascending=False)

    total_sales = cat_summary["Total_Sales"].sum()
    cat_summary["Share"] = (cat_summary["Total_Sales"] / total_sales) * 100
    cat_summary["Margin"] = (cat_summary["Total_Profit"] / cat_summary["Total_Sales"]) * 100

    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)

    palette = ["#1F4E79", "#2E75B6", "#5DADE2", "#A9CCE3"][:len(cat_summary)]
    explode = [0.03] * len(cat_summary)

    wedges, texts, autotexts = ax.pie(
        cat_summary["Total_Sales"],
        labels=cat_summary["Category"],
        autopct="%1.1f%%",
        pctdistance=0.78,
        startangle=140,
        colors=palette,
        explode=explode,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
        textprops=dict(fontsize=11, fontweight="bold")
    )

    # Styling percentage labels
    for at in autotexts:
        at.set_color("white")
        at.set_fontsize(10)
        at.set_fontweight("bold")

    # Center circle annotation
    ax.text(0, 0.08, "Total Sales", ha="center", va="center", fontsize=11, color="#7F8C8D", fontweight="bold")
    ax.text(0, -0.08, f"${total_sales:,.0f}", ha="center", va="center", fontsize=15, fontweight="bold", color="#1F4E79")

    # Legend with profit margin callouts
    legend_labels = [f"{row['Category']}: ${row['Total_Sales']:,.0f} (Margin: {row['Margin']:.1f}%)"
                     for _, row in cat_summary.iterrows()]
    ax.legend(wedges, legend_labels, title="Category Sales & Margins", loc="lower center",
              bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=True, fontsize=9)

    ax.set_title("Category Revenue Contribution & Profit Margins", fontsize=14,
                 fontweight="bold", pad=20, color="#1F4E79")

    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, "03_category_sales_donut.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Saved: {out_path}")


def plot_regional_performance(df):
    """Chart 4: Regional Performance Comparison (Clustered Bar Chart)"""
    reg_summary = df.groupby("Region").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    ).reset_index().sort_values("Total_Sales", ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

    x = range(len(reg_summary))
    width = 0.35

    bars1 = ax.bar([i - width/2 for i in x], reg_summary["Total_Sales"], width,
                   label="Sales ($)", color="#1F4E79", edgecolor="#333333", lw=0.6)
    bars2 = ax.bar([i + width/2 for i in x], reg_summary["Total_Profit"], width,
                   label="Profit ($)", color="#2CA02C", edgecolor="#333333", lw=0.6)

    ax.set_title("Regional Commercial Breakdown: Sales vs. Net Profit",
                 fontsize=14, fontweight="bold", pad=15, color="#1F4E79")
    ax.set_xticks(list(x))
    ax.set_xticklabels(reg_summary["Region"], fontsize=11, fontweight="bold")
    ax.set_ylabel("USD ($)", fontsize=11, fontweight="bold")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: f"${y * 1e-3:.0f}K"))

    # Value labels
    for bar in bars1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 1500, f"${h * 1e-3:.1f}K",
                ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#1F4E79")

    for bar in bars2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 1500, f"${h * 1e-3:.1f}K",
                ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#2CA02C")

    ax.set_ylim(0, max(reg_summary["Total_Sales"]) * 1.18)
    ax.legend(loc="upper right", frameon=True, fontsize=10)
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, "04_regional_performance.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Saved: {out_path}")


def main():
    print("Loading data from SQLite...")
    df = load_data()
    print(f"Loaded {len(df):,} transaction records.")

    print("Generating charts...")
    plot_sales_trend(df)
    plot_top_5_products(df)
    plot_category_donut(df)
    plot_regional_performance(df)
    print("All charts generated and saved successfully in visuals/ folder!")


if __name__ == "__main__":
    main()
