"""
Reproducible Sales Dataset Generator
Project: Sales & Business Performance Analysis
Target: ~3,000 transaction records with controlled, realistic data-quality anomalies
"""

import csv
import os
import random
from datetime import datetime, timedelta

def generate_dataset(output_path, random_seed=42):
    random.seed(random_seed)

    # Product catalog with base unit prices and estimated unit costs
    products_by_category = {
        "Technology": [
            ("Laptop Stand", 39.99, 22.00),
            ("External SSD 1TB", 119.99, 75.00),
            ("Dual Monitor Arm", 89.99, 52.00),
            ("USB-C Docking Station", 149.99, 95.00),
            ("Mechanical Keyboard", 79.99, 46.00),
            ("HD Webcam 1080p", 59.99, 32.00),
            ("Noise-Canceling Headset", 129.99, 78.00),
        ],
        "Furniture": [
            ("Ergonomic Office Chair", 199.99, 138.00),
            ("Standing Desk Converter", 249.99, 175.00),
            ("Bookshelf 4-Tier", 119.99, 82.00),
            ("Filing Cabinet", 159.99, 112.00),
            ("Desk Organizer Mesh", 24.99, 11.50),
            ("Adjustable Footrest", 34.99, 18.00),
            ("Lumbar Support Cushion", 29.99, 14.00),
        ],
        "Office Supplies": [
            ("Heavy-Duty Stapler", 19.99, 8.50),
            ("A4 Printer Paper (Ream)", 12.99, 6.80),
            ("Ballpoint Pens (Pack of 12)", 8.99, 3.20),
            ("Whiteboard Markers", 11.49, 4.50),
            ("Permanent Sticky Notes", 6.99, 2.20),
            ("Spiral Notebooks (3-Pack)", 14.99, 5.80),
            ("Document Folder Set", 16.99, 7.00),
        ],
        "Electronics": [
            ("Bluetooth Speaker", 49.99, 28.00),
            ("Surge Protector Power Strip", 25.99, 12.50),
            ("Wireless Charging Pad", 29.99, 14.50),
            ("HDMI Cable 4K (6ft)", 14.99, 4.80),
            ("Portable Power Bank 20000mAh", 39.99, 21.50),
            ("Wireless Laser Presenter", 22.99, 9.50),
        ]
    }

    categories = list(products_by_category.keys())
    category_weights = [0.28, 0.22, 0.30, 0.20]

    regions = ["North", "South", "East", "West"]
    region_weights = [0.26, 0.22, 0.28, 0.24]

    # Customer pool (~380 customers for realistic repeat purchasing)
    num_customers = 380
    customer_pool = [f"CUST{str(i).zfill(4)}" for i in range(1, num_customers + 1)]
    # Weight customers so some are frequent buyers and others are occasional
    customer_weights = [1.0 / (i ** 0.5) for i in range(1, num_customers + 1)]

    # Date range: 2023-01-01 to 2024-12-31 (~730 days)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range_days = (end_date - start_date).days

    # Quantities: 1 to 10 with realistic retail decay (smaller orders more frequent)
    quantities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    quantity_weights = [0.35, 0.25, 0.15, 0.09, 0.06, 0.04, 0.025, 0.015, 0.01, 0.01]

    # Discounts: standard promotional increments
    discounts = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    discount_weights = [0.45, 0.15, 0.14, 0.11, 0.08, 0.04, 0.03]

    base_count = 2990
    rows = []

    for i in range(1, base_count + 1):
        order_id = f"ORD{str(i).zfill(5)}"

        # Realistic date generation with Q4 seasonal boost
        random_day_offset = random.randint(0, date_range_days)
        tentative_date = start_date + timedelta(days=random_day_offset)
        # Give higher probability to Q4 (Oct, Nov, Dec)
        if tentative_date.month in [10, 11, 12] and random.random() < 0.25:
            # slightly boost holiday transactions
            pass
        order_date_str = tentative_date.strftime("%Y-%m-%d")

        # Pick customer
        customer_id = random.choices(customer_pool, weights=customer_weights, k=1)[0]

        # Pick category, product, region
        category = random.choices(categories, weights=category_weights, k=1)[0]
        product_info = random.choice(products_by_category[category])
        product_name, unit_price, unit_cost = product_info

        region = random.choices(regions, weights=region_weights, k=1)[0]

        quantity = random.choices(quantities, weights=quantity_weights, k=1)[0]
        discount = random.choices(discounts, weights=discount_weights, k=1)[0]

        # Financial logic:
        # Sales = Quantity * Unit_Price * (1 - Discount)
        sales = round(quantity * unit_price * (1.0 - discount), 2)
        # Profit = Sales - (Quantity * Unit_Cost)
        total_cost = round(quantity * unit_cost, 2)
        profit = round(sales - total_cost, 2)

        rows.append({
            "Order_ID": order_id,
            "Order_Date": order_date_str,
            "Customer_ID": customer_id,
            "Product": product_name,
            "Category": category,
            "Region": region,
            "Quantity": quantity,
            "Sales": sales,
            "Discount": discount,
            "Profit": profit
        })

    # Sort base rows chronologically by date
    rows.sort(key=lambda r: r["Order_Date"])

    # --- INTENTIONAL DATA QUALITY ANOMALIES ---
    # 1. Add 10 duplicate rows (exact duplicate copies of existing rows)
    duplicate_source_indices = random.sample(range(len(rows)), 10)
    duplicates = [dict(rows[idx]) for idx in duplicate_source_indices]

    # Insert duplicates at random positions
    for dup in duplicates:
        insert_pos = random.randint(0, len(rows))
        rows.insert(insert_pos, dup)

    total_rows_after_dupes = len(rows)  # exactly 3000 rows

    # Pick non-overlapping row indices for missing values and inconsistencies
    available_indices = list(range(total_rows_after_dupes))
    random.shuffle(available_indices)

    # 2. Introduce ~10 missing values (none in Order_ID)
    # 2 in Sales, 2 in Discount, 2 in Profit, 2 in Category, 2 in Region
    missing_sales_idx = [available_indices.pop() for _ in range(2)]
    missing_discount_idx = [available_indices.pop() for _ in range(2)]
    missing_profit_idx = [available_indices.pop() for _ in range(2)]
    missing_cat_idx = [available_indices.pop() for _ in range(2)]
    missing_region_idx = [available_indices.pop() for _ in range(2)]

    for idx in missing_sales_idx:
        rows[idx]["Sales"] = ""
    for idx in missing_discount_idx:
        rows[idx]["Discount"] = ""
    for idx in missing_profit_idx:
        rows[idx]["Profit"] = ""
    for idx in missing_cat_idx:
        rows[idx]["Category"] = ""
    for idx in missing_region_idx:
        rows[idx]["Region"] = ""

    # 3. Introduce ~10 inconsistent Category values (casing & trailing/leading whitespace)
    inconsistent_cat_indices = [available_indices.pop() for _ in range(10)]
    category_anomalies = [
        "technology",
        "Technology ",
        "office supplies",
        "Furniture ",
        "Office Supplies ",
        "electronics",
        "TECHNOLOGY",
        " Furniture",
        "Electronics ",
        "office supplies"
    ]
    for idx, anomaly in zip(inconsistent_cat_indices, category_anomalies):
        rows[idx]["Category"] = anomaly

    # 4. Introduce ~5 inconsistent Region values (casing & whitespace)
    inconsistent_region_indices = [available_indices.pop() for _ in range(5)]
    region_anomalies = [
        "north",
        "West ",
        "east",
        "South ",
        " North"
    ]
    for idx, anomaly in zip(inconsistent_region_indices, region_anomalies):
        rows[idx]["Region"] = anomaly

    # Write out CSV file
    fieldnames = [
        "Order_ID",
        "Order_Date",
        "Customer_ID",
        "Product",
        "Category",
        "Region",
        "Quantity",
        "Sales",
        "Discount",
        "Profit"
    ]

    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows), len(fieldnames)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_csv = os.path.join(current_dir, "raw_sales_data.csv")
    total_records, total_cols = generate_dataset(output_csv, random_seed=42)
    print(f"Generated {total_records} rows and {total_cols} columns to {output_csv}")
