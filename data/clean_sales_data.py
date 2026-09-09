"""
Data Cleaning & SQLite Database Setup Script
Project: Sales & Business Performance Analysis

Tasks:
1. Load raw sales data from data/raw_sales_data.csv.
2. Remove duplicate transaction rows.
3. Standardize casing and strip whitespace from Category and Region.
4. Impute missing Category values from Product catalog.
5. Impute missing Region values based on Customer transaction history.
6. Impute missing financial values (Sales, Discount, Profit) using unit prices and costs.
7. Save cleaned data to data/processed/sales_data_cleaned.csv.
8. Create SQLite database at sql/sales_analysis.db and populate the sales_data table.
"""

import os
import csv
import sqlite3
from collections import defaultdict, Counter

# Product catalog reference for pricing, cost, and category mapping
PRODUCT_CATALOG = {
    # Technology
    "Laptop Stand": {"category": "Technology", "unit_price": 39.99, "unit_cost": 22.00},
    "External SSD 1TB": {"category": "Technology", "unit_price": 119.99, "unit_cost": 75.00},
    "Dual Monitor Arm": {"category": "Technology", "unit_price": 89.99, "unit_cost": 52.00},
    "USB-C Docking Station": {"category": "Technology", "unit_price": 149.99, "unit_cost": 95.00},
    "Mechanical Keyboard": {"category": "Technology", "unit_price": 79.99, "unit_cost": 46.00},
    "HD Webcam 1080p": {"category": "Technology", "unit_price": 59.99, "unit_cost": 32.00},
    "Noise-Canceling Headset": {"category": "Technology", "unit_price": 129.99, "unit_cost": 78.00},
    # Furniture
    "Ergonomic Office Chair": {"category": "Furniture", "unit_price": 199.99, "unit_cost": 138.00},
    "Standing Desk Converter": {"category": "Furniture", "unit_price": 249.99, "unit_cost": 175.00},
    "Bookshelf 4-Tier": {"category": "Furniture", "unit_price": 119.99, "unit_cost": 82.00},
    "Filing Cabinet": {"category": "Furniture", "unit_price": 159.99, "unit_cost": 112.00},
    "Desk Organizer Mesh": {"category": "Furniture", "unit_price": 24.99, "unit_cost": 11.50},
    "Adjustable Footrest": {"category": "Furniture", "unit_price": 34.99, "unit_cost": 18.00},
    "Lumbar Support Cushion": {"category": "Furniture", "unit_price": 29.99, "unit_cost": 14.00},
    # Office Supplies
    "Heavy-Duty Stapler": {"category": "Office Supplies", "unit_price": 19.99, "unit_cost": 8.50},
    "A4 Printer Paper (Ream)": {"category": "Office Supplies", "unit_price": 12.99, "unit_cost": 6.80},
    "Ballpoint Pens (Pack of 12)": {"category": "Office Supplies", "unit_price": 8.99, "unit_cost": 3.20},
    "Whiteboard Markers": {"category": "Office Supplies", "unit_price": 11.49, "unit_cost": 4.50},
    "Permanent Sticky Notes": {"category": "Office Supplies", "unit_price": 6.99, "unit_cost": 2.20},
    "Spiral Notebooks (3-Pack)": {"category": "Office Supplies", "unit_price": 14.99, "unit_cost": 5.80},
    "Document Folder Set": {"category": "Office Supplies", "unit_price": 16.99, "unit_cost": 7.00},
    # Electronics
    "Bluetooth Speaker": {"category": "Electronics", "unit_price": 49.99, "unit_cost": 28.00},
    "Surge Protector Power Strip": {"category": "Electronics", "unit_price": 25.99, "unit_cost": 12.50},
    "Wireless Charging Pad": {"category": "Electronics", "unit_price": 29.99, "unit_cost": 14.50},
    "HDMI Cable 4K (6ft)": {"category": "Electronics", "unit_price": 14.99, "unit_cost": 4.80},
    "Portable Power Bank 20000mAh": {"category": "Electronics", "unit_price": 39.99, "unit_cost": 21.50},
    "Wireless Laser Presenter": {"category": "Electronics", "unit_price": 22.99, "unit_cost": 9.50},
}

CANONICAL_CATEGORIES = {
    "technology": "Technology",
    "furniture": "Furniture",
    "office supplies": "Office Supplies",
    "electronics": "Electronics"
}

CANONICAL_REGIONS = {
    "north": "North",
    "south": "South",
    "east": "East",
    "west": "West"
}


def clean_dataset(raw_csv_path, cleaned_csv_path):
    print(f"Reading raw data from: {raw_csv_path}")
    with open(raw_csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        raw_rows = list(reader)

    initial_count = len(raw_rows)
    print(f"Initial raw rows: {initial_count}")

    # 1. Remove exact duplicates & duplicated Order_IDs
    unique_rows = []
    seen_order_ids = set()
    duplicate_count = 0

    for row in raw_rows:
        order_id = row["Order_ID"].strip()
        if order_id in seen_order_ids:
            duplicate_count += 1
            continue
        seen_order_ids.add(order_id)
        unique_rows.append(row)

    print(f"Duplicate rows removed: {duplicate_count}")
    print(f"Rows remaining after deduplication: {len(unique_rows)}")

    # Pre-pass: Map customer to their most frequent known region
    customer_regions = defaultdict(list)
    for row in unique_rows:
        reg = row["Region"].strip().lower()
        if reg in CANONICAL_REGIONS:
            customer_regions[row["Customer_ID"].strip()].append(CANONICAL_REGIONS[reg])

    cleaned_rows = []
    cleaned_metrics = {
        "category_standardized": 0,
        "category_imputed": 0,
        "region_standardized": 0,
        "region_imputed": 0,
        "sales_imputed": 0,
        "discount_imputed": 0,
        "profit_imputed": 0
    }

    for row in unique_rows:
        order_id = row["Order_ID"].strip()
        order_date = row["Order_Date"].strip()
        customer_id = row["Customer_ID"].strip()
        product = row["Product"].strip()

        prod_meta = PRODUCT_CATALOG.get(product, {})
        unit_price = prod_meta.get("unit_price", 0.0)
        unit_cost = prod_meta.get("unit_cost", 0.0)
        expected_category = prod_meta.get("category", "")

        # Category cleaning
        raw_cat = row["Category"].strip()
        if not raw_cat:
            category = expected_category
            cleaned_metrics["category_imputed"] += 1
        else:
            cat_lower = raw_cat.lower()
            if cat_lower in CANONICAL_CATEGORIES:
                category = CANONICAL_CATEGORIES[cat_lower]
                if raw_cat != category:
                    cleaned_metrics["category_standardized"] += 1
            else:
                category = expected_category
                cleaned_metrics["category_standardized"] += 1

        # Region cleaning
        raw_reg = row["Region"].strip()
        if not raw_reg:
            # Impute from customer history or default to most common region
            known_regs = customer_regions.get(customer_id, [])
            if known_regs:
                category_mode = Counter(known_regs).most_common(1)[0][0]
                region = category_mode
            else:
                region = "East"
            cleaned_metrics["region_imputed"] += 1
        else:
            reg_lower = raw_reg.lower()
            if reg_lower in CANONICAL_REGIONS:
                region = CANONICAL_REGIONS[reg_lower]
                if raw_reg != region:
                    cleaned_metrics["region_standardized"] += 1
            else:
                region = "East"
                cleaned_metrics["region_standardized"] += 1

        # Quantity
        quantity = int(row["Quantity"].strip())

        # Discount
        raw_discount = row["Discount"].strip()
        raw_sales = row["Sales"].strip()
        raw_profit = row["Profit"].strip()

        if raw_discount:
            discount = float(raw_discount)
        else:
            # Impute discount
            if raw_sales:
                # discount = 1 - (sales / (quantity * unit_price))
                gross = quantity * unit_price
                sales_val = float(raw_sales)
                discount = max(0.0, round((gross - sales_val) / gross, 2))
            else:
                discount = 0.0
            cleaned_metrics["discount_imputed"] += 1

        # Sales
        if raw_sales:
            sales = float(raw_sales)
        else:
            sales = round(quantity * unit_price * (1.0 - discount), 2)
            cleaned_metrics["sales_imputed"] += 1

        # Profit
        if raw_profit:
            profit = float(raw_profit)
        else:
            total_cost = quantity * unit_cost
            profit = round(sales - total_cost, 2)
            cleaned_metrics["profit_imputed"] += 1

        cleaned_rows.append({
            "Order_ID": order_id,
            "Order_Date": order_date,
            "Customer_ID": customer_id,
            "Product": product,
            "Category": category,
            "Region": region,
            "Quantity": quantity,
            "Sales": round(sales, 2),
            "Discount": round(discount, 2),
            "Profit": round(profit, 2)
        })

    # Sort cleaned rows chronologically
    cleaned_rows.sort(key=lambda r: r["Order_Date"])

    # Ensure output directory exists
    os.makedirs(os.path.dirname(cleaned_csv_path), exist_ok=True)

    fieldnames = [
        "Order_ID", "Order_Date", "Customer_ID", "Product",
        "Category", "Region", "Quantity", "Sales", "Discount", "Profit"
    ]

    with open(cleaned_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print(f"Cleaned data successfully saved to: {cleaned_csv_path}")
    print(f"Cleaning summary metrics: {cleaned_metrics}")
    return cleaned_rows


def create_sqlite_database(cleaned_rows, db_path):
    print(f"Creating SQLite database at: {db_path}")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table sales_data
    cursor.execute("""
        CREATE TABLE sales_data (
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

    # Insert cleaned records
    insert_sql = """
        INSERT INTO sales_data (
            Order_ID, Order_Date, Customer_ID, Product,
            Category, Region, Quantity, Sales, Discount, Profit
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    records_to_insert = [
        (
            r["Order_ID"],
            r["Order_Date"],
            r["Customer_ID"],
            r["Product"],
            r["Category"],
            r["Region"],
            r["Quantity"],
            r["Sales"],
            r["Discount"],
            r["Profit"]
        )
        for r in cleaned_rows
    ]

    cursor.executemany(insert_sql, records_to_insert)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM sales_data;")
    count = cursor.fetchone()[0]
    print(f"Successfully inserted {count} rows into table 'sales_data' in {db_path}")

    conn.close()
    return count


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw_sales_data.csv")
    cleaned_path = os.path.join(base_dir, "data", "processed", "sales_data_cleaned.csv")
    db_path = os.path.join(base_dir, "sql", "sales_analysis.db")

    cleaned_data = clean_dataset(raw_path, cleaned_path)
    inserted_count = create_sqlite_database(cleaned_data, db_path)
    print(f"Done! Cleaned rows: {len(cleaned_data)}, Database records: {inserted_count}")
