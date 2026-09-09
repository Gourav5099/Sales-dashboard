# 📝 Raw Data Quality Notes
**Dataset**: `data/raw_sales_data.csv`  
**Purpose**: Documenting the intentional real-world data anomalies seeded into the raw dataset for the data cleaning phase (Excel & SQL).

---

## 🔍 Overview

In realistic enterprise environments, source sales data extracted from transactional systems or third-party POS channels rarely arrives in pristine condition. To mirror an authentic Data Analyst challenge and demonstrate practical cleaning techniques, a controlled number of realistic data quality defects have been intentionally introduced.

> **Note**: Exact row numbers and primary keys are deliberately omitted from these notes so that data cleaning exercises (filtering, conditional formatting, deduplication, and SQL validation queries) can be genuinely practiced and demonstrated during evaluation.

---

## ⚠️ Summary of Intentional Data Quality Issues

### 1. Duplicate Transaction Rows (~10 rows)
- **Nature of Issue**: Complete duplicate records where all column values (including `Order_ID`, date, customer, product, and financial values) are identical copies of another transaction in the file.
- **Real-World Cause**: Double-entry by POS terminals, API retry glitches, or batch ETL duplication.
- **Cleaning Objective**: Identify duplicate records using Excel's *Remove Duplicates* feature or SQL `ROW_NUMBER() OVER (PARTITION BY Order_ID ...)` queries to retain only unique transactions.

---

### 2. Missing (Null/Blank) Values (~10 instances)
- **Nature of Issue**: Empty strings (`""`) present in non-key fields. `Order_ID` is strictly preserved without nulls to ensure primary transaction tracking is maintained.
- **Distribution**:
  - **Financial Metrics** (`Sales`, `Discount`, `Profit`): A few blank entries in monetary fields where recalculation or imputation is required based on related fields ($\text{Sales} = \text{Quantity} \times \text{Price} \times (1 - \text{Discount})$).
  - **Categorical Fields** (`Category`, `Region`): A few blank records requiring lookup inference (e.g., inferring Category from known Product names) or flagging as "Unspecified".
- **Real-World Cause**: Network dropouts during transaction logging, unmapped product SKUs, or optional form fields.

---

### 3. Inconsistent Category Formatting (~10 rows)
- **Nature of Issue**: Casing variations and whitespace anomalies across the four core categories (`Technology`, `Furniture`, `Office Supplies`, `Electronics`).
- **Examples Encountered**:
  - Lowercase variations (e.g., `technology`, `office supplies`, `electronics`).
  - Leading or trailing whitespace (e.g., `"Furniture "`, `" Office Supplies"`).
  - Uppercase variation (e.g., `TECHNOLOGY`).
- **Real-World Cause**: Free-text entry by sales reps, unstandardized POS dropdowns, or legacy system imports.
- **Cleaning Objective**: Standardize using `TRIM()`, `PROPER()`, or SQL `INITCAP()` / `CASE` statements to prevent fragmented groupings in Pivot Tables and BI models.

---

### 4. Inconsistent Region Formatting (~5 rows)
- **Nature of Issue**: Case discrepancies and accidental spacing in sales territories (`North`, `South`, `East`, `West`).
- **Examples Encountered**:
  - Lowercase variations (e.g., `north`, `east`).
  - Spacing artifacts (e.g., `"West "`, `" North"`).
- **Real-World Cause**: Multiple legacy branch regional tagging rules.
- **Cleaning Objective**: Cleanse using text manipulation functions and mapping tables prior to loading into Power BI / Tableau.

---

## 📊 Summary Table of Data Integrity

| Category of Quality Issue | Approximate Count | Target Columns Affected | Recommended Cleaning Tool |
| :--- | :---: | :--- | :--- |
| **Exact Duplicate Rows** | ~10 | All columns | Excel Data Tools / SQL CTE Window Functions |
| **Missing Financials** | ~6 | `Sales`, `Discount`, `Profit` | Excel Formulas (`IF`, `ROUND`) / SQL `COALESCE` / Imputation |
| **Missing Dimensions** | ~4 | `Category`, `Region` | Excel `XLOOKUP` from Product / SQL `UPDATE JOIN` |
| **Inconsistent Category Text**| ~10 | `Category` | Excel `TRIM`, `PROPER` / SQL `TRIM`, `UPPER` |
| **Inconsistent Region Text** | ~5 | `Region` | Excel `TRIM`, `PROPER` / SQL `TRIM`, `UPPER` |

> **Audit Outcome**: Over **98.8%** of the records are clean and valid out-of-the-box, ensuring business patterns, seasonality, and KPI calculations remain statistically sound while providing meaningful cleaning tasks.
