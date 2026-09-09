"""
Load Cleaned Data to SQLite and Execute Data Analyst Queries
Project: Sales & Business Performance Analysis
"""

import os
import csv
import sqlite3
from datetime import datetime

def find_cleaned_file(base_dir):
    candidates = [
        os.path.join(base_dir, "sales_data_cleaning.csv"),
        os.path.join(base_dir, "excel", "sales_data_cleaning.xlsx.csv"),
        os.path.join(base_dir, "excel", "sales_data_cleaning.csv"),
        os.path.join(base_dir, "sql", "sales_data_cleaning.csv"),
        os.path.join(base_dir, "data", "sales_data_cleaning.csv"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    raise FileNotFoundError("Could not find sales_data_cleaning.csv in known directories.")

def parse_date(date_str):
    date_str = date_str.strip()
    # Try ISO format
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass
    # Try M/D/YYYY
    try:
        dt = datetime.strptime(date_str, "%m/%d/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass
    # Try D/M/YYYY
    try:
        dt = datetime.strptime(date_str, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return date_str

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)

    source_csv = find_cleaned_file(base_dir)
    print(f"Loading cleaned sales data from: {source_csv}")

    # Also copy to root/sql as standard sales_data_cleaning.csv if not there
    target_clean_copy = os.path.join(base_dir, "sales_data_cleaning.csv")
    if not os.path.exists(target_clean_copy) and source_csv != target_clean_copy:
        import shutil
        shutil.copy2(source_csv, target_clean_copy)

    db_path = os.path.join(base_dir, "sql", "sales_analysis.db")
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales_data (
        Order_ID VARCHAR(20) PRIMARY KEY,
        Order_Date DATE NOT NULL,
        Customer_ID VARCHAR(20) NOT NULL,
        Product VARCHAR(100) NOT NULL,
        Category VARCHAR(50) NOT NULL,
        Region VARCHAR(20) NOT NULL,
        Quantity INTEGER NOT NULL,
        Sales REAL NOT NULL,
        Discount REAL NOT NULL,
        Profit REAL NOT NULL
    );
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_category ON sales_data(Category);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_region ON sales_data(Region);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_order_date ON sales_data(Order_Date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_product ON sales_data(Product);")

    # Read and insert records
    with open(source_csv, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        records = []
        seen_order_ids = set()
        duplicate_skips = 0

        for row in reader:
            order_id = row["Order_ID"].strip()
            if not order_id:
                continue
            if order_id in seen_order_ids:
                duplicate_skips += 1
                continue
            seen_order_ids.add(order_id)

            order_date = parse_date(row["Order_Date"])
            customer_id = row["Customer_ID"].strip()
            product = row["Product"].strip()
            category = row["Category"].strip()
            region = row["Region"].strip()
            quantity = int(float(row["Quantity"].strip())) if row["Quantity"].strip() else 1
            sales = round(float(row["Sales"].strip()), 2) if row["Sales"].strip() else 0.0
            discount = round(float(row["Discount"].strip()), 2) if row["Discount"].strip() else 0.0
            profit = round(float(row["Profit"].strip()), 2) if row["Profit"].strip() else 0.0

            records.append((
                order_id, order_date, customer_id, product, category,
                region, quantity, sales, discount, profit
            ))

    cursor.executemany("""
    INSERT INTO sales_data (
        Order_ID, Order_Date, Customer_ID, Product, Category,
        Region, Quantity, Sales, Discount, Profit
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, records)

    conn.commit()
    total_loaded = len(records)
    print(f"Loaded {total_loaded} rows into sales_data table (skipped {duplicate_skips} duplicate Order_IDs).")

    # Run queries
    # Query 1: Total Sales & Total Profit
    q1 = """
    SELECT 
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Overall_Profit_Margin_Pct,
        COUNT(DISTINCT Order_ID) AS Total_Orders,
        COUNT(DISTINCT Customer_ID) AS Total_Customers,
        SUM(Quantity) AS Total_Units_Sold,
        ROUND(AVG(Sales), 2) AS Avg_Order_Value
    FROM sales_data;
    """
    cursor.execute(q1)
    q1_res = cursor.fetchone()

    # Query 2: Top 5 Products by Sales
    q2 = """
    SELECT 
        Product,
        Category,
        SUM(Quantity) AS Units_Sold,
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin_Pct
    FROM sales_data
    GROUP BY Product, Category
    ORDER BY Total_Sales DESC
    LIMIT 5;
    """
    cursor.execute(q2)
    q2_res = cursor.fetchall()

    # Query 3: Category and Region-wise Sales Breakdown
    q3 = """
    SELECT 
        Category,
        Region,
        COUNT(DISTINCT Order_ID) AS Total_Orders,
        SUM(Quantity) AS Units_Sold,
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin_Pct
    FROM sales_data
    GROUP BY Category, Region
    ORDER BY Category ASC, Total_Sales DESC;
    """
    cursor.execute(q3)
    q3_res = cursor.fetchall()

    # Query 4: Category Summary
    q4 = """
    SELECT 
        Category,
        COUNT(DISTINCT Order_ID) AS Total_Orders,
        SUM(Quantity) AS Units_Sold,
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin_Pct
    FROM sales_data
    GROUP BY Category
    ORDER BY Total_Sales DESC;
    """
    cursor.execute(q4)
    q4_res = cursor.fetchall()

    # Query 5: Regional Summary
    q5 = """
    SELECT 
        Region,
        COUNT(DISTINCT Order_ID) AS Total_Orders,
        SUM(Quantity) AS Units_Sold,
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin_Pct
    FROM sales_data
    GROUP BY Region
    ORDER BY Total_Sales DESC;
    """
    cursor.execute(q5)
    q5_res = cursor.fetchall()

    # Write QUERY_RESULTS.md
    out_md = os.path.join(base_dir, "sql", "QUERY_RESULTS.md")

    with open(out_md, mode="w", encoding="utf-8") as f:
        f.write("# 📊 SQL Query Execution Results\n\n")
        f.write(f"**Database**: `sql/sales_analysis.db`  \n")
        f.write(f"**Source Data**: `sales_data_cleaning.csv`  \n")
        f.write(f"**Total Verified Transactions Loaded**: **{total_loaded:,}**  \n\n")
        f.write("---\n\n")

        # Section 1
        f.write("## 1. Overall Business Performance (Total Sales & Profit)\n\n")
        f.write("```sql\n" + q1.strip() + "\n```\n\n")
        f.write("| Total Sales | Total Profit | Profit Margin (%) | Total Orders | Unique Customers | Total Units Sold | Avg Order Value |\n")
        f.write("| :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
        f.write(f"| **${q1_res[0]:,.2f}** | **${q1_res[1]:,.2f}** | **{q1_res[2]}%** | {q1_res[3]:,} | {q1_res[4]:,} | {q1_res[5]:,} | ${q1_res[6]:,.2f} |\n\n")
        f.write("> **Key Finding**: The business generated **${:,.2f}** in total sales with **${:,.2f}** in net profit, representing a healthy overall profit margin of **{}%** and an Average Order Value (AOV) of **${:,.2f}**.\n\n".format(
            q1_res[0], q1_res[1], q1_res[2], q1_res[6]
        ))
        f.write("---\n\n")

        # Section 2
        f.write("## 2. Top 5 Products by Total Sales\n\n")
        f.write("```sql\n" + q2.strip() + "\n```\n\n")
        f.write("| Rank | Product | Category | Units Sold | Total Sales ($) | Total Profit ($) | Profit Margin (%) |\n")
        f.write("| :---: | :--- | :--- | :---: | :---: | :---: | :---: |\n")
        for rank, row in enumerate(q2_res, 1):
            f.write(f"| {rank} | **{row[0]}** | {row[1]} | {row[2]:,} | ${row[3]:,.2f} | ${row[4]:,.2f} | {row[5]}% |\n")
        f.write("\n> **Key Finding**: **{}** is the top revenue generator (${:,.2f}), followed by **{}** (${:,.2f}). Both demonstrate solid positive margins.\n\n".format(
            q2_res[0][0], q2_res[0][3], q2_res[1][0], q2_res[1][3]
        ))
        f.write("---\n\n")

        # Section 3
        f.write("## 3. Category and Region-wise Sales Breakdown\n\n")
        f.write("```sql\n" + q3.strip() + "\n```\n\n")
        f.write("| Category | Region | Total Orders | Units Sold | Total Sales ($) | Total Profit ($) | Profit Margin (%) |\n")
        f.write("| :--- | :--- | :---: | :---: | :---: | :---: | :---: |\n")
        for row in q3_res:
            f.write(f"| {row[0]} | {row[1]} | {row[2]:,} | {row[3]:,} | ${row[4]:,.2f} | ${row[5]:,.2f} | {row[6]}% |\n")
        f.write("\n---\n\n")

        # Section 4
        f.write("## 4. Supplementary Summaries\n\n")
        f.write("### A. Category Performance Summary\n\n")
        f.write("| Category | Orders | Units Sold | Total Sales ($) | Total Profit ($) | Profit Margin (%) |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: |\n")
        for row in q4_res:
            f.write(f"| **{row[0]}** | {row[1]:,} | {row[2]:,} | ${row[3]:,.2f} | ${row[4]:,.2f} | {row[5]}% |\n")

        f.write("\n### B. Regional Performance Summary\n\n")
        f.write("| Region | Orders | Units Sold | Total Sales ($) | Total Profit ($) | Profit Margin (%) |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: |\n")
        for row in q5_res:
            f.write(f"| **{row[0]}** | {row[1]:,} | {row[2]:,} | ${row[3]:,.2f} | ${row[4]:,.2f} | {row[5]}% |\n")

    conn.close()
    print(f"Results successfully saved to {out_md}")

if __name__ == "__main__":
    main()
