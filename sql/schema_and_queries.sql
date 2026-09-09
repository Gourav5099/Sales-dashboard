-- ==============================================================================
-- Project: Sales & Business Performance Analysis
-- Database: sales_analysis.db
-- Table: sales_data
-- Purpose: Schema setup and core analytical SQL queries for academic evaluation
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. TABLE CREATION SCHEMA
-- ------------------------------------------------------------------------------
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

-- Index creation for optimized analytical querying
CREATE INDEX IF NOT EXISTS idx_sales_category ON sales_data(Category);
CREATE INDEX IF NOT EXISTS idx_sales_region ON sales_data(Region);
CREATE INDEX IF NOT EXISTS idx_sales_order_date ON sales_data(Order_Date);
CREATE INDEX IF NOT EXISTS idx_sales_product ON sales_data(Product);


-- ------------------------------------------------------------------------------
-- 2. CORE BUSINESS QUERIES
-- ------------------------------------------------------------------------------

-- Query 1: Total Sales & Total Profit (Overall Business Performance)
SELECT 
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Overall_Profit_Margin_Pct,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    COUNT(DISTINCT Customer_ID) AS Total_Customers,
    SUM(Quantity) AS Total_Units_Sold,
    ROUND(AVG(Sales), 2) AS Avg_Order_Value
FROM sales_data;


-- Query 2: Top 5 Products by Total Sales
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


-- Query 3: Sales & Profit Breakdown by Category and Region
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


-- ------------------------------------------------------------------------------
-- 3. SUPPLEMENTARY HIGH-LEVEL KPI QUERIES
-- ------------------------------------------------------------------------------

-- Query 4: Category-Level Performance Summary
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


-- Query 5: Region-Level Performance Summary
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
