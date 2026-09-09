# 📊 Executive Presentation Summary: Sales & Business Performance Analysis

**Author**: Junior Data Analyst Candidate  
**Project**: Sales & Business Performance Analysis  
**Evaluation Scope**: Academic Viva Voce & Student Data Analyst Portfolio  
**Deliverables Staged**: Cleaned Dataset, SQLite Database, SQL Analytical Scripts, Power BI Architecture  

---

## 🎯 1. Executive Summary

This project presents a rigorous, business-driven diagnostic analysis of a multi-regional retail and e-commerce business over a 24-month trading window (January 2023 – December 2024).

Starting from a transactional dataset containing controlled real-world anomalies, the data was scrubbed and validated in **Excel**, staged into an **SQLite** relational database, analyzed with production-standard **SQL** queries, and structured for executive visual storytelling in **Power BI**.

### Core Headline Metrics

```text
┌───────────────────────┬───────────────────────┬───────────────────────┐
│     TOTAL REVENUE     │      NET PROFIT       │     PROFIT MARGIN     │
│      $450,978.56      │      $157,745.23      │        34.98%         │
├───────────────────────┼───────────────────────┼───────────────────────┤
│     TOTAL ORDERS      │   UNIQUE CUSTOMERS    │   AVG ORDER VALUE     │
│      2,990 Orders     │     380 Customers     │        $150.83        │
└───────────────────────┴───────────────────────┴───────────────────────┘
```

---

## 🔍 2. Data Cleaning & Validation Audit

| Stage | Input Records | Output Records | Key Interventions |
| :--- | :---: | :---: | :--- |
| **Raw Ingestion** | 3,000 | 3,000 | Ingested `data/raw_sales_data.csv` with seeded data quality defects. |
| **Deduplication** | 3,000 | **2,990** | Removed 10 exact duplicate records based on unique `Order_ID`. |
| **Text Standardization** | 2,990 | 2,990 | Cleared trailing whitespace and normalized casing for Categories and Regions. |
| **Missing Imputation** | 2,990 | 2,990 | Re-derived missing Sales/Profit/Discounts using base product price and cost rules. |
| **SQL Staging** | 2,990 | 2,990 | Inserted validated records into `sales_data` table in `sql/sales_analysis.db`. |

---

## 📈 3. Key Findings & Commercial Insights

### A. Category Revenue vs. Profitability Paradox

| Category | Total Orders | Units Sold | Total Revenue ($) | Net Profit ($) | Profit Margin (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Technology** | 830 | 2,122 | **\$189,018.44** | **\$66,695.42** | **35.29%** |
| **Furniture** | 622 | 1,684 | **\$183,965.24** | **\$51,943.84** | **28.24%** |
| **Electronics** | 597 | 1,631 | **\$46,543.94** | **\$21,917.84** | **47.09%** |
| **Office Supplies** | 934 | 2,400 | **\$30,524.93** | **\$16,867.62** | **55.26%** |

- **Volume vs Margin Insight**: **Technology** and **Furniture** drive **82.7%** of gross enterprise sales, but **Office Supplies** and **Electronics** yield significantly higher profit margins (**55.26%** and **47.09%** respectively).
- **Furniture Margin Warning**: Furniture has the lowest margin (28.24%) because heavy promotional discounts (>20%) applied to high base cost items erode profitability.

---

### B. Top 5 Revenue-Driving Products

| Rank | Product Name | Category | Units Sold | Total Sales ($) | Total Profit ($) | Profit Margin (%) |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **1** | **Standing Desk Converter** | Furniture | 267 | **\$62,784.93** | \$16,059.93 | 25.58% |
| **2** | **USB-C Docking Station** | Technology | 291 | **\$41,037.18** | \$13,392.18 | 32.63% |
| **3** | **Ergonomic Office Chair** | Furniture | 209 | **\$38,728.02** | \$9,886.02 | 25.53% |
| **4** | **Noise-Canceling Headset** | Technology | 322 | **\$38,009.04** | \$12,893.04 | 33.92% |
| **5** | **External SSD 1TB** | Technology | 328 | **\$35,834.91** | \$11,234.91 | 31.35% |

---

### C. Geographic Territory Performance

| Region | Total Orders | Units Sold | Total Sales ($) | Net Profit ($) | Margin (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **East** | 826 | 2,097 | **\$121,757.68** | **\$42,952.11** | **35.28%** |
| **North** | 790 | 2,047 | **\$116,403.30** | **\$40,696.00** | **34.96%** |
| **West** | 698 | 1,901 | **\$108,201.06** | **\$38,131.99** | **35.24%** |
| **South** | 672 | 1,793 | **\$104,223.63** | **\$35,792.74** | **34.34%** |

- Sales performance is balanced, with **East** and **North** leading commercial volume.
- Margins across all 4 territories remain remarkably consistent (~34.3% to 35.3%), confirming stable regional pricing discipline.

---

## 💡 4. Actionable Business Recommendations

Based on empirical data analysis, four high-impact strategic initiatives are recommended:

1. **Implement a 15% Maximum Discount Cap on Furniture**:
   - High-cost items like *Standing Desk Converters* and *Ergonomic Chairs* currently experience substantial margin deterioration during promotional campaigns. Restricting discounts to $\le 15\%$ will preserve approximately **\$4,200 to \$6,500** in quarterly profit.
2. **Bundle High-Margin Office Supplies with Technology Hardware**:
   - Capitalize on the **55.26% margin** of Office Supplies by offering bundled add-ons (e.g., notebook and organizer sets) at checkout when customers purchase docking stations or laptops. This immediately raises the Average Order Value (AOV) without discounting core hardware.
3. **Targeted Expansion in Southern & Western Territories**:
   - The South region currently lags East by \$17.5K in sales despite comparable margin health (34.34%). Allocating digital marketing spend toward B2B regional accounts in the South will capture untapped demand.
4. **Institutionalize a Tiered B2B Customer Loyalty Program**:
   - 380 unique customers placed 2,990 orders (averaging 7.8 orders per customer). Establishing annual volume rebate tiers will protect high-frequency corporate buyers from churn.

---

## 📂 5. Project Artifacts & Verification Directory

| Artifact | File Location | Purpose |
| :--- | :--- | :--- |
| **Cleaned Dataset** | [`sales_data_cleaning.csv`](file:///c:/Users/pango/Downloads/GOURAV''S%20PROJECT/sales_data_cleaning.csv) | 2,990 verified transaction records ready for analytics |
| **SQLite Database** | [`sql/sales_analysis.db`](file:///c:/Users/pango/Downloads/GOURAV''S%20PROJECT/sql/sales_analysis.db) | Relational database containing indexed `sales_data` table |
| **SQL Queries** | [`sql/schema_and_queries.sql`](file:///c:/Users/pango/Downloads/GOURAV''S%20PROJECT/sql/schema_and_queries.sql) | DDL schema and analytical SQL queries |
| **Query Output** | [`sql/QUERY_RESULTS.md`](file:///c:/Users/pango/Downloads/GOURAV''S%20PROJECT/sql/QUERY_RESULTS.md) | Formatted query execution tables and statistical outputs |
| **Power BI Specs** | [`powerbi/README.md`](file:///c:/Users/pango/Downloads/GOURAV''S%20PROJECT/powerbi/README.md) | Star schema design, DAX measures code, and page layouts |
| **Viva Voce Guide** | [`documentation/VIVA_VOCE_GUIDE.md`](file:///c:/Users/pango/Downloads/GOURAV''S%20PROJECT/documentation/VIVA_VOCE_GUIDE.md) | Complete interview Q&A and methodology justifications |
| **Project Schema** | [`DATASET_SCHEMA.md`](file:///c:/Users/pango/Downloads/GOURAV''S%20PROJECT/DATASET_SCHEMA.md) | 10-column data dictionary and constraint definitions |
