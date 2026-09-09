# 🎓 Comprehensive Viva Voce Preparation Guide

**Project Title**: Sales & Business Performance Analysis  
**Role**: Junior Data Analyst (College Level / Academic Defense)  
**Tools Evaluated**: Excel, SQL (SQLite), Power BI, Tableau  

---

## 📑 Table of Contents
1. [2-Minute Elevator Pitch](#1-2-minute-project-elevator-pitch)
2. [Key Business Metrics & Dataset Numbers](#2-key-business-metrics--dataset-numbers)
3. [Technical Choices Justification](#3-technical-choices-justification)
4. [Excel Technical Questions & Answers](#4-excel-technical-questions--answers)
5. [SQL Technical Questions & Answers](#5-sql-technical-questions--answers)
6. [Power BI & DAX Technical Questions & Answers](#6-power-bi--dax-technical-questions--answers)
7. [Tableau & Visual Storytelling Questions & Answers](#7-tableau--visual-storytelling-questions--answers)
8. [Data Cleaning & Edge Cases Defense](#8-data-cleaning--edge-cases-defense)
9. [Future Recommendations & Next Steps](#9-future-recommendations--next-steps)

---

## 🎙️ 1. 2-Minute Project Elevator Pitch

> *"In this project, titled **'Sales & Business Performance Analysis'**, I simulated the end-to-end workflow of a Junior Data Analyst analyzing commercial operations for a mid-sized retail and e-commerce business across a 2-year period (2023–2024).*
>
> *I began by ingesting 3,000 raw transaction records that contained controlled real-world data quality defects—such as exact duplicate orders, inconsistent text casing, whitespace discrepancies, and missing financial values. Using **Excel** and structured data cleaning workflows, I resolved all anomalies, standardized formats, and validated 2,990 clean transactions.*
>
> *Next, I staged the cleaned dataset into a relational **SQLite** database (`sales_analysis.db`) and constructed optimized SQL scripts featuring aggregations, grouping, and indexing. The analysis revealed **\$450,978.56** in total sales and **\$157,745.23** in net profit, demonstrating an overall profit margin of **34.98%** and an Average Order Value of **\$150.83**.*
>
> *Finally, I designed a **Star Schema** BI model in **Power BI**, engineered robust DAX measures (`DIVIDE`, `CALCULATE`, `DATEADD` for Month-over-Month growth), and planned interactive multi-page dashboards to help executives identify high-margin opportunities and control discount erosion.*
>
> *The entire architecture deliberately avoids unnecessary complexity like machine learning or cloud services, focusing purely on practical, production-standard business intelligence."*

---

## 📊 2. Key Business Metrics & Dataset Numbers

Memorize these verified figures for your presentation:

| Metric | Verified Value | Business Meaning |
| :--- | :---: | :--- |
| **Total Revenue / Sales** | **\$450,978.56** | Gross revenue generated across all completed orders |
| **Total Net Profit** | **\$157,745.23** | Net margin after subtracting product unit costs |
| **Overall Profit Margin** | **34.98%** | Net Profit $\div$ Total Sales |
| **Total Transactions (Clean)**| **2,990** | Total order lines (deduplicated from 3,000 raw rows) |
| **Unique Customer Pool** | **380** | Demonstrates solid repeat purchasing (~7.8 orders/customer) |
| **Total Units Sold** | **7,849 units** | Physical inventory moved |
| **Average Order Value (AOV)** | **\$150.83** | Average transaction size across all categories |
| **Top Revenue Product** | **Standing Desk Converter** | **\$62,784.93** Sales (267 units sold, 25.58% margin) |
| **Top Revenue Category** | **Technology** | **\$189,018.44** Sales (35.29% profit margin) |
| **Highest Margin Category** | **Office Supplies** | **55.26% Margin** (high-margin, lower unit-price category) |
| **Top Sales Region** | **East** | **\$121,757.68** Sales (35.28% margin) |

---

## 💡 3. Technical Choices Justification

### Q: Why SQLite instead of MySQL, PostgreSQL, or SQL Server?
- **Zero Configuration & Self-Contained**: SQLite runs in-process as a single file (`sales_analysis.db`), eliminating server configuration and credential dependencies.
- **Portability for Evaluation**: Examiners and peers can inspect and query the database instantly without needing a running database service.
- **Standard SQL Compliance**: SQLite fully supports ANSI SQL standards, including primary keys, constraints, CTEs, window functions, and indexing.

### Q: Why build a Star Schema instead of using one flat table in Power BI?
- **Storage & Ingestion Efficiency**: Fact-dimension separation eliminates repetitive dimensional text, reducing memory usage in the VertiPaq engine.
- **Simpler DAX**: Filter context flows cleanly down 1-to-Many relationships from Dimensions (`Dim_Calendar`, `Dim_Product`, `Dim_Region`) to the Fact table (`sales_data`).
- **Standard Enterprise Best Practice**: Mirrors how enterprise data warehouses (Snowflake, BigQuery) structure data marts.

### Q: Why did you perform data cleaning in both Excel and SQL?
- **Excel's Role**: Ideal for initial exploratory profiling, visual spot-checking of headers, filtering for blanks, and quick validation.
- **SQL's Role**: Provides automated, auditable, and repeatable transformations through scripted DDL and DML queries.

---

## 📗 4. Excel Technical Questions & Answers

### Q1: How did you identify and handle duplicate records in Excel?
**Answer**:  
I used Excel's built-in **Data > Remove Duplicates** tool after selecting all columns. For auditability, I first highlighted duplicates using **Conditional Formatting > Highlight Cells Rules > Duplicate Values** on the `Order_ID` column. 10 duplicate rows were identified and removed.

### Q2: How did you fix inconsistent text casing and whitespace?
**Answer**:  
- **Whitespace**: Applied the `=TRIM(text)` function to remove accidental leading and trailing spaces (e.g., converting `"Furniture "` to `"Furniture"`).
- **Casing**: Used `=PROPER(text)` to standardize lowercase entries (e.g., `technology` to `Technology`).
- **Validation**: Replaced formulas with their static values using **Paste Special > Values**.

### Q3: What is the difference between `VLOOKUP` and `XLOOKUP`?
**Answer**:  
- `VLOOKUP` requires the lookup column to be the leftmost column, uses a fragile static column index number, and defaults to approximate match unless `FALSE` is specified.
- `XLOOKUP` can look in any direction (left or right), does not break when columns are inserted or deleted, defaults to exact match, and provides a built-in `if_not_found` argument.

---

## 🗄️ 5. SQL Technical Questions & Answers

### Q1: Can you explain the query you wrote for Top 5 Products by Sales?
**Answer**:
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
- **Aggregation**: `SUM(Sales)` sums total revenue per group.
- **Grouping**: `GROUP BY Product, Category` aggregates records at the product grain while retaining category context.
- **Sorting & Limiting**: `ORDER BY Total_Sales DESC LIMIT 5` orders the aggregated revenue descending and returns the top 5 records.

### Q2: What is the difference between `WHERE` and `HAVING`?
**Answer**:  
- `WHERE` filters individual rows **before** any aggregation takes place.
- `HAVING` filters aggregated grouped results **after** `GROUP BY` has executed (e.g., `HAVING SUM(Sales) > 50000`).

### Q3: Why did you create indexes on `Category`, `Region`, and `Order_Date`?
**Answer**:  
Indexes create B-tree lookup structures in SQLite. Because analytical queries repeatedly filter and group by Category, Region, and Date, indexes transform full-table scans ($O(N)$) into logarithmic lookups ($O(\log N)$), significantly improving query speed.

### Q4: How would you calculate Month-over-Month (MoM) growth using SQL?
**Answer**:  
By using a Common Table Expression (CTE) combined with the `LAG()` window function:
```sql
WITH MonthlySales AS (
    SELECT 
        strftime('%Y-%m', Order_Date) AS Month_Year,
        SUM(Sales) AS Monthly_Revenue
    FROM sales_data
    GROUP BY strftime('%Y-%m', Order_Date)
)
SELECT 
    Month_Year,
    Monthly_Revenue,
    LAG(Monthly_Revenue, 1) OVER (ORDER BY Month_Year) AS Prior_Month_Revenue,
    ROUND(((Monthly_Revenue - LAG(Monthly_Revenue, 1) OVER (ORDER BY Month_Year)) 
          / LAG(Monthly_Revenue, 1) OVER (ORDER BY Month_Year)) * 100, 2) AS MoM_Growth_Pct
FROM MonthlySales;
```

---

## 📈 6. Power BI & DAX Technical Questions & Answers

### Q1: Why did you use `DIVIDE()` instead of the standard `/` division operator?
**Answer**:  
In DAX, `[Total Profit] / [Total Sales]` returns `NaN` or `Infinity` if `[Total Sales]` is 0. The `DIVIDE([Total Profit], [Total Sales], 0)` function intercepts divide-by-zero scenarios and gracefully returns the third argument (0) without failing report visuals.

### Q2: What is the difference between a Calculated Column and a Measure?
| Feature | Calculated Column | Measure |
| :--- | :--- | :--- |
| **Evaluation Context** | Row context (during data refresh) | Filter context (dynamically on visual render) |
| **RAM / File Size** | Increases file size & memory usage | Consumes zero persistent storage |
| **Use Case** | Slicers, categorical row labels | Aggregations, KPIs, ratios, percentages |

### Q3: What is the purpose of `CALCULATE()` in DAX?
**Answer**:  
`CALCULATE()` is the most critical function in DAX. It evaluates an expression under a modified filter context. For example:
```dax
Technology Sales = CALCULATE([Total Sales], sales_data[Category] = "Technology")
```
It overrides or merges existing visual filters with the explicit condition specified.

### Q4: Why is a dedicated Calendar/Date table necessary?
**Answer**:  
Time-intelligence functions such as `DATEADD()`, `SAMEPERIODLASTYEAR()`, and `TOTALYTD()` require a continuous, gap-free date range. Without a dedicated calendar table, missing dates in transactional records cause time-intelligence calculations to return inaccurate numbers.

---

## 📊 7. Tableau & Visual Storytelling Questions & Answers

### Q1: What is the difference between Blue pills and Green pills in Tableau?
**Answer**:  
- **Blue pills** represent **Discrete** fields (create headers, row/column dividers, categories).
- **Green pills** represent **Continuous** fields (create continuous numeric axes, gradients, time lines).
*(A common mistake is thinking Blue = Dimension and Green = Measure; while common, dimensions can be continuous and measures can be discrete).*

### Q2: What are Level of Detail (LOD) Expressions in Tableau?
**Answer**:  
LOD expressions allow computing aggregations at a different level of granularity than the visual view:
- **FIXED**: Computes value using specified dimensions without reference to view dimensions.
- **INCLUDE**: Computes value at a more granular level than the view.
- **EXCLUDE**: Computes value ignoring specific view dimensions.

---

## 🧼 8. Data Cleaning & Edge Cases Defense

### Q: Why are some profit values negative in the dataset? Is that a bug?
**Answer**:  
No, negative profit is intentional and realistic in retail. When high promotional discounts (e.g., 25%–30%) are applied to products where base gross margin is less than the discount rate, net earnings fall below zero. Identifying these loss-making transactions allows analysts to recommend discount caps to protect profitability.

### Q: How did you handle missing values in Category and Financials?
**Answer**:  
- **Category**: Inferred 100% accurately by mapping the existing `Product` name against the known product catalog.
- **Financials**: Re-derived using exact business rules:
  $$\text{Sales} = \text{Quantity} \times \text{Unit Price} \times (1 - \text{Discount})$$
  $$\text{Profit} = \text{Sales} - (\text{Quantity} \times \text{Unit Cost})$$

---

## 🎯 9. Future Recommendations & Next Steps

When examiners ask *"What would you add to this project if given another month?"*:
1. **Automated ETL Pipeline**: Replace manual CSV export with an automated Python/Airflow script that extracts data from POS endpoints directly into the database.
2. **Customer Cohort Analysis**: Track customer retention and repeat purchase behavior across cohorts over their 2-year lifecycle.
3. **Advanced Pricing Optimization**: Build an elasticity model to determine the exact discount threshold where promotional volume outweighs margin reduction.
