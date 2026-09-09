# 📊 SQL Query Execution Results

**Database**: `sql/sales_analysis.db`  
**Source Data**: `sales_data_cleaning.csv`  
**Total Verified Transactions Loaded**: **2,990**  

---

## 1. Overall Business Performance (Total Sales & Profit)

```sql
SELECT 
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Overall_Profit_Margin_Pct,
        COUNT(DISTINCT Order_ID) AS Total_Orders,
        COUNT(DISTINCT Customer_ID) AS Total_Customers,
        SUM(Quantity) AS Total_Units_Sold,
        ROUND(AVG(Sales), 2) AS Avg_Order_Value
    FROM sales_data;
```

| Total Sales | Total Profit | Profit Margin (%) | Total Orders | Unique Customers | Total Units Sold | Avg Order Value |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$450,978.56** | **$157,745.23** | **34.98%** | 2,990 | 380 | 7,849 | $150.83 |

> **Key Finding**: The business generated **$450,978.56** in total sales with **$157,745.23** in net profit, representing a healthy overall profit margin of **34.98%** and an Average Order Value (AOV) of **$150.83**.

---

## 2. Top 5 Products by Total Sales

```sql
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
```

| Rank | Product | Category | Units Sold | Total Sales ($) | Total Profit ($) | Profit Margin (%) |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| 1 | **Standing Desk Converter** | Furniture | 267 | $62,784.93 | $16,059.93 | 25.58% |
| 2 | **USB-C Docking Station** | Technology | 291 | $41,037.18 | $13,392.18 | 32.63% |
| 3 | **Ergonomic Office Chair** | Furniture | 209 | $38,728.02 | $9,886.02 | 25.53% |
| 4 | **Noise-Canceling Headset** | Technology | 322 | $38,009.04 | $12,893.04 | 33.92% |
| 5 | **External SSD 1TB** | Technology | 328 | $35,834.91 | $11,234.91 | 31.35% |

> **Key Finding**: **Standing Desk Converter** is the top revenue generator ($62,784.93), followed by **USB-C Docking Station** ($41,037.18). Both demonstrate solid positive margins.

---

## 3. Category and Region-wise Sales Breakdown

```sql
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
```

| Category | Region | Total Orders | Units Sold | Total Sales ($) | Total Profit ($) | Profit Margin (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
|  | North | 1 | 2 | $79.98 | $36.98 | 46.24% |
|  | West | 1 | 3 | $59.97 | $34.47 | 57.48% |
| Electronics | North | 182 | 493 | $13,527.57 | $6,559.37 | 48.49% |
| Electronics | East | 162 | 403 | $11,750.15 | $5,422.25 | 46.15% |
| Electronics | South | 122 | 381 | $10,880.93 | $5,172.83 | 47.54% |
| Electronics | West | 129 | 347 | $10,217.36 | $4,666.96 | 45.68% |
| Electronics | east | 1 | 6 | $137.94 | $80.94 | 58.68% |
| Electronics | north | 1 | 1 | $29.99 | $15.49 | 51.65% |
| Furniture | East | 171 | 441 | $47,848.45 | $14,120.95 | 29.51% |
| Furniture | North | 154 | 402 | $46,527.11 | $12,741.21 | 27.38% |
| Furniture | South | 146 | 411 | $45,015.36 | $11,916.36 | 26.47% |
| Furniture | West | 150 | 427 | $44,469.35 | $13,114.35 | 29.49% |
| Furniture |  | 1 | 3 | $104.97 | $50.97 | 48.56% |
| Office Supplies | East | 256 | 653 | $8,724.22 | $4,678.08 | 53.62% |
| Office Supplies | North | 242 | 641 | $8,213.97 | $4,552.27 | 55.42% |
| Office Supplies | West | 220 | 584 | $7,201.45 | $4,080.28 | 56.66% |
| Office Supplies | South | 216 | 522 | $6,385.29 | $3,556.99 | 55.71% |
| TECHNOLOGY | South | 1 | 1 | $127.49 | $32.49 | 25.48% |
| Technology | East | 237 | 600 | $53,434.86 | $18,730.83 | 35.05% |
| Technology | North | 208 | 504 | $47,404.72 | $16,593.72 | 35.0% |
| Technology | West | 198 | 540 | $46,252.93 | $16,235.93 | 35.1% |
| Technology | South | 186 | 477 | $41,805.94 | $15,109.95 | 36.14% |
| Technology |  | 1 | 1 | $119.99 | $24.99 | 20.83% |
| electronics | South | 1 | 1 | $8.62 | $4.12 | 47.8% |
| office supplies | North | 2 | 4 | $626.96 | $198.96 | 31.73% |
| technology | North | 1 | 1 | $22.99 | $13.49 | 58.68% |

---

## 4. Supplementary Summaries

### A. Category Performance Summary

| Category | Orders | Units Sold | Total Sales ($) | Total Profit ($) | Profit Margin (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Technology** | 830 | 2,122 | $189,018.44 | $66,695.42 | 35.29% |
| **Furniture** | 622 | 1,684 | $183,965.24 | $51,943.84 | 28.24% |
| **Electronics** | 597 | 1,631 | $46,543.94 | $21,917.84 | 47.09% |
| **Office Supplies** | 934 | 2,400 | $30,524.93 | $16,867.62 | 55.26% |
| **office supplies** | 2 | 4 | $626.96 | $198.96 | 31.73% |
| **** | 2 | 5 | $139.95 | $71.45 | 51.05% |
| **TECHNOLOGY** | 1 | 1 | $127.49 | $32.49 | 25.48% |
| **technology** | 1 | 1 | $22.99 | $13.49 | 58.68% |
| **electronics** | 1 | 1 | $8.62 | $4.12 | 47.8% |

### B. Regional Performance Summary

| Region | Orders | Units Sold | Total Sales ($) | Total Profit ($) | Profit Margin (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **East** | 826 | 2,097 | $121,757.68 | $42,952.11 | 35.28% |
| **North** | 790 | 2,047 | $116,403.30 | $40,696.00 | 34.96% |
| **West** | 698 | 1,901 | $108,201.06 | $38,131.99 | 35.24% |
| **South** | 672 | 1,793 | $104,223.63 | $35,792.74 | 34.34% |
| **** | 2 | 4 | $224.96 | $75.96 | 33.77% |
| **east** | 1 | 6 | $137.94 | $80.94 | 58.68% |
| **north** | 1 | 1 | $29.99 | $15.49 | 51.65% |
