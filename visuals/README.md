# 📈 Executive Dashboard Visualizations

This directory contains high-resolution (300 DPI) visual charts generated from our SQLite database (`sql/sales_analysis.db`) using Python, Matplotlib, and Pandas.

---

## 🖼️ Gallery of Generated Visualizations

### 1. Total Sales & Profit Performance Trend
**File**: [`01_sales_trend.png`](file:///c:/Users/pango/Downloads/GOURAV''S%20PROJECT/visuals/01_sales_trend.png)  
**Chart Type**: Dual Line Chart with Area Fill  
- **Visual Description**: Traces the 24-month timeline (January 2023 to December 2024), illustrating monthly revenue alongside net profit.
- **Key Insight**: Demonstrates healthy, consistent profit tracking with prominent sales spikes during September/Q4 trading periods.

---

### 2. Top 5 Revenue-Generating Products
**File**: [`02_top_5_products.png`](file:///c:/Users/pango/Downloads/GOURAV''S%20PROJECT/visuals/02_top_5_products.png)  
**Chart Type**: Horizontal Bar Chart with Value Labels & Margins  
- **Visual Description**: Ranks the top 5 products by gross revenue, annotated with exact sales figures and profit margins.
- **Key Insight**: **Standing Desk Converter** ($62.78K) and **USB-C Docking Station** ($41.17K) lead total enterprise revenue.

---

### 3. Category Revenue Contribution & Profit Margins
**File**: [`03_category_sales_donut.png`](file:///c:/Users/pango/Downloads/GOURAV''S%20PROJECT/visuals/03_category_sales_donut.png)  
**Chart Type**: Donut Chart with Center KPI Callout  
- **Visual Description**: Proportional breakdown of enterprise sales across the 4 core categories, highlighting total sales ($450,979) in the center.
- **Key Insight**: **Technology** (41.9%) and **Furniture** (41.1%) generate over 80% of sales volume, while **Office Supplies** (55.9%) and **Electronics** (47.1%) deliver the highest profit margins.

---

### 4. Regional Commercial Breakdown
**File**: [`04_regional_performance.png`](file:///c:/Users/pango/Downloads/GOURAV''S%20PROJECT/visuals/04_regional_performance.png)  
**Chart Type**: Clustered Column Chart  
- **Visual Description**: Side-by-side comparison of total sales vs net profit across East, North, West, and South territories.
- **Key Insight**: The **East** region leads overall sales ($122.1K), while profitability rates remain stable (~35%) across all four regions.

---

## ⚙️ How to Regenerate Charts

Run the automated Python script from the project root:
```bash
python visuals/generate_charts.py
```
