# 📋 Dataset Schema & Data Dictionary

**Project**: Sales & Business Performance Analysis  
**Target Scope**: Small-to-medium retail / e-commerce business  
**Target Volume**: ~3,000 transaction records  
**Granularity**: Each record represents a single product line item in a customer order  

---

## 1. Overview of Dataset Columns

The raw transactional dataset consists of **exactly 10 columns**:

| # | Column Name | Business Description |
| :---: | :--- | :--- |
| **1** | `Order_ID` | Unique identifier for each transaction/order line |
| **2** | `Order_Date` | The calendar date on which the purchase occurred |
| **3** | `Customer_ID` | Unique identifier representing the purchasing customer |
| **4** | `Product` | The descriptive name of the specific item purchased |
| **5** | `Category` | High-level commercial grouping of the product |
| **6** | `Region` | Commercial sales territory where the order was placed |
| **7** | `Quantity` | Number of units purchased in the transaction |
| **8** | `Sales` | Total revenue generated from the transaction ($) |
| **9** | `Discount` | Discount rate applied to the order (decimal ratio) |
| **10** | `Profit` | Net monetary earnings from the order line ($) |

---

## 2. Comprehensive Data Dictionary

| Column Name | SQL Data Type | Excel / BI Type | Example Value | Nullable | Value Constraints / Range | Business Purpose |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| `Order_ID` | `VARCHAR(20)` | Text | `ORD-2023-1042` | No | Prefix `ORD-` followed by year and sequential number | Serves as the primary transaction key; tracks total orders and order frequency. |
| `Order_Date` | `DATE` | Date (`YYYY-MM-DD`) | `2023-04-18` | No | Spans 2 years (e.g., `2023-01-01` to `2024-12-31`) | Facilitates time-series analysis: monthly trends, seasonality, MoM & YoY growth. |
| `Customer_ID` | `VARCHAR(15)` | Text | `CUST-0312` | No | Prefix `CUST-` followed by zero-padded ID (`CUST-0001` to `CUST-0400`) | Enables customer segmentation, repeat purchase analysis, and customer lifetime order metrics. |
| `Product` | `VARCHAR(100)` | Text | `Ergonomic Office Chair` | No | Standardized product title mapped to one Category | Analyzes top-selling vs. underperforming individual items. |
| `Category` | `VARCHAR(50)` | Text | `Furniture` | No | Allowed: `Technology`, `Furniture`, `Office Supplies`, `Electronics` | Groups products for higher-level performance comparison and portfolio balancing. |
| `Region` | `VARCHAR(20)` | Text | `West` | No | Allowed: `North`, `South`, `East`, `West` | Enables regional distribution comparison and geographical drill-downs. |
| `Quantity` | `INT` | Whole Number | `3` | No | Positive integer: `1` to `10` units | Tracks physical volume sold; used to calculate Average Units per Order. |
| `Sales` | `DECIMAL(10,2)` | Currency / Decimal | `449.97` | No | Positive float $> 0.00$ ($\text{Qty} \times \text{Unit Price} \times (1 - \text{Discount})$) | Core commercial metric: represents gross monetary revenue generated. |
| `Discount` | `DECIMAL(4,2)` | Percentage / Decimal | `0.15` (15%) | No | Float between `0.00` and `0.35` (0% to 35%) | Measures pricing strategies and discount impact on margins and sales volume. |
| `Profit` | `DECIMAL(10,2)` | Currency / Decimal | `67.50` | No | Numeric float (Can be positive, zero, or negative) | Core profitability metric: identifies loss-making transactions and healthy margins. |

---

## 3. Allowed Categorical Dimensions

### Categories & Associated Products

To ensure realism for a small-to-medium retail company, products are distributed across the four designated categories:

1. **Technology**:
   - Laptop Stand, External SSD 1TB, Dual Monitor Arm, USB-C Docking Station, Mechanical Keyboard, HD Webcam 1080p, Noise-Canceling Headset.
2. **Furniture**:
   - Ergonomic Office Chair, Standing Desk Converter, Bookshelf 4-Tier, Filing Cabinet, Desk Organizer Mesh, Adjustable Footrest, Lumbar Support Cushion.
3. **Office Supplies**:
   - Heavy-Duty Stapler, A4 Printer Paper (Ream), Ballpoint Pens (Pack of 12), Whiteboard Markers, Permanent Sticky Notes, Spiral Notebooks, Document Folder Set.
4. **Electronics**:
   - Bluetooth Speaker, Surge Protector Power Strip, Wireless Charging Pad, HDMI Cable 4K (6ft), Portable Power Bank 20000mAh, Wireless Laser Presenter.

### Regions

The business operates across four standard sales regions:
- **North**
- **South**
- **East**
- **West**

---

## 4. Business Rules & Metric Calculation Logic

1. **Sales Calculation**:
   $$\text{Sales} = \text{Quantity} \times \text{Unit Price} \times (1 - \text{Discount})$$
   *(Rounded to 2 decimal places)*

2. **Profit Calculation**:
   $$\text{Profit} = \text{Sales} - (\text{Quantity} \times \text{Unit Cost})$$
   *(Negative profit occurs realistically when high discounts are applied to products with lower profit margins)*

3. **Profit Margin (%)**:
   $$\text{Profit Margin} = \left( \frac{\text{Profit}}{\text{Sales}} \right) \times 100$$

4. **Data Realism Guidelines**:
   - **Discount Thresholds**: Orders with $0\%$ to $10\%$ discount typically yield solid positive profits. Orders with discounts $> 25\%$ occasionally result in negative profit (loss leaders or margin erosion).
   - **Customer Distribution**: ~300 to 400 distinct customers across 3,000 orders to enable repeat purchase behavior (e.g., 20–30% of customers placing multiple orders).
   - **Date Distribution**: Distributed across a 24-month horizon (2023–2024) with natural holiday seasonality in Q4 (October–December).

---

## 5. Academic & Viva Voce Talking Points

- **Why is the dataset designed at the line-item grain?**  
  Having one row per product line item allows granular aggregation at both the order level (summing sales for a single `Order_ID`) and the product/category level without duplicate counting issues.
- **Why is negative profit included?**  
  In real-world retail businesses, discounts, promotions, and clearance sales often generate transactions where revenue is below cost. Identifying these loss-making items is one of the most critical responsibilities of a business data analyst.
- **Why are exactly 10 columns chosen?**  
  These 10 columns contain all essential dimensions (Time, Geography, Product, Customer) and facts (Quantity, Sales, Discount, Profit) required to compute standard business KPIs without introducing unnecessary database complexity.
