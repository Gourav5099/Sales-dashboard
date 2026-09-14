import os
import re

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORT_MD = os.path.join(PROJECT_ROOT, "documentation", "SUMMER_TRAINING_REPORT.md")
DOCS_REPORT_MD = os.path.join(PROJECT_ROOT, "docs", "SUMMER_TRAINING_REPORT.md")
MASTER_MD = os.path.join(PROJECT_ROOT, "documentation", "MASTER_APPENDIX.md")
DOCS_MASTER_MD = os.path.join(PROJECT_ROOT, "docs", "MASTER_APPENDIX.md")

appendix_a_text = """## Appendix A: Software and Tools Used

This appendix outlines the complete hardware, operating system, application software, programming runtimes, libraries, and development tools utilized across the design, engineering, execution, and presentation phases of the **Sales & Business Performance Analysis** project.

### A.1 Hardware & Operating System Specifications
- **Host Operating System**: Microsoft Windows 11 Home / Professional (64-bit Architecture, x64-based processor).
- **Processor**: Intel Core i5 / i7 (or AMD Ryzen equivalent) with multi-threading support.
- **System Memory (RAM)**: 16.0 GB DDR4/DDR5 high-bandwidth memory (supporting in-memory Power BI VertiPaq tabular caching and Streamlit local server execution).
- **Secondary Storage**: High-speed NVMe Solid State Drive (SSD) with >= 5.0 GB dedicated storage for repository assets, database staging, and visualization artifacts.

### A.2 Core Software Applications & Analytical Platforms
| Software / Platform | Vendor / Organization | Version | Operational Function & Implementation Scope |
| :--- | :--- | :---: | :--- |
| **Microsoft Excel** | Microsoft Corporation | Office 365 / 2021 | Preliminary exploratory data auditing, sanity checking, conditional formatting rules, duplicate identification, and Pivot Table validation. |
| **SQLite Database Engine** | SQLite Development Team | 3.45.1+ | Serverless, zero-configuration relational database staging (`sql/sales_analysis.db`). Implemented with B-Tree indexes on categorical and temporal fields for ANSI SQL query execution. |
| **Microsoft Power BI Desktop**| Microsoft Corporation | 2.128.0+ | Enterprise dimensional modeling (Star Schema), VertiPaq columnar compression, dynamic DAX calculation engine, and 3-page interactive visual dashboard creation. |
| **Tableau Desktop / Public** | Salesforce, Inc. | 2024.1+ | VizQL visual analytics, multi-dimensional exploratory data analysis, dual-axis margin comparison charts, and visual storytelling. |
| **Visual Studio Code (VS Code)**| Microsoft Corporation | 1.90.0+ | Primary Integrated Development Environment (IDE) for Python scripting, SQL query editing, Git branch management, and markdown report drafting. |
| **Google Chrome / Edge** | Google LLC / Microsoft Corp | 128.0+ | Modern web browser interface for testing local Streamlit reactive apps (`localhost:8501`) and headless Chromium PDF report generation engine. |

### A.3 Programming Languages, Runtimes & Dependency Libraries
- **Primary Language & Runtime**: **Python 3.13.x (64-bit)**.
- **Dependency Specification (`requirements.txt`)**:
  - `streamlit>=1.30.0`: High-performance reactive web framework providing sidebar filters, dynamic KPI metric cards, and responsive session state management.
  - `pandas>=2.0.0`: Fast in-memory tabular data manipulation, vectorized arithmetic, datetime parsing, GroupBy aggregations, and CSV I/O handling.
  - `plotly>=5.18.0`: Interactive JavaScript-backed declarative charting engine rendering interactive tooltips, hover highlights, and zoomable visual layouts.
  - `matplotlib>=3.8.0`: Foundational 2D visualization library used to construct 300 DPI publication-grade static figures (`visuals/generate_charts.py`).
  - `markdown>=3.10.0` & `pygments>=2.21.0`: Text-to-HTML parser and syntax highlighting engine used to automate academic report compilation.

### A.4 Version Control, Collaboration & Staging Environment
- **Git**: Version 2.44+ distributed source control system managing branch tracking, semantic commit history, and code lineage.
- **GitHub**: Cloud repository hosting platform (`https://github.com/Gourav5099/Sales-dashboard`) facilitating public portfolio sharing, cloud CI/CD integration, and one-click Streamlit Community Cloud deployment.
- **Streamlit Community Cloud**: Cloud serverless hosting platform deploying `app.py` for permanent global web access.

### A.5 Cross-Platform Capability & Comparative Tool Matrix
| Operational Feature | Microsoft Excel | SQLite RDBMS | Microsoft Power BI | Tableau Desktop | Python (Streamlit + Plotly) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Data Scalability Limit** | 1,048,576 rows | Terabytes (disk) | High (In-memory compressed) | High (Hyper extract engine) | High (RAM bound / Chunked) |
| **Analytical Language** | Spreadsheet formulas | ANSI SQL | DAX & Power Query M | VizQL / Calculated Fields | Python / Pandas vectorized |
| **Interactivity Level** | Medium (Slicers) | None (CLI / Text) | Very High (Cross-filtering) | Very High (Actions/Filters) | High (Reactive Python state) |
| **Automated Scripting** | Low (VBA/Macros) | High (SQL scripts) | Medium (Scheduled refresh) | Medium (Tableau Prep) | Full (Automated CLI/APIs) |
| **Licensing / Cost** | Paid Commercial | 100% Free / Open Source | Free Desktop / Paid Pro | Paid Commercial | 100% Free / Open Source |
"""

appendix_b_text = """## Appendix B: Project Modules & Architectural Breakdown

The **Sales & Business Performance Analysis** system is architected as an end-to-end, six-tier modular pipeline. Each module encapsulates distinct business logic, input criteria, transformation rules, and output deliverables:

```text
+--------------------------------------------------------------------------------------------------+
|                         END-TO-END PROJECT MODULAR ARCHITECTURE                                  |
+--------------------------------------------------------------------------------------------------+
|  [MODULE 1: Synthetic Data Generation Engine]                                                    |
|  Script: data/generate_sales_data.py | Ingests config -> Generates 3,000 raw transactional rows  |
|  Seeded Anomalies: 10 exact duplicates, 10 nulls, 15 text casing defects, whitespace errors      |
+--------------------------------------------------------------------------------------------------+
|                                                |                                                 |
|                                                v                                                 |
|  [MODULE 2: Data Cleansing, Hygiene & Transformation Engine]                                     |
|  Script / Pipeline: sales_data_cleaning.csv                                                      |
|  Processes: Deduplication (2,990 clean rows), Deterministic formula imputation, Title Casing     |
+--------------------------------------------------------------------------------------------------+
|                                                |                                                 |
|                                                v                                                 |
|  [MODULE 3: Relational Database Staging & SQL Analytical Execution Engine]                       |
|  Database: sql/sales_analysis.db | Schema: sales_data with B-Tree Indexes                        |
|  Queries: 5 Core Analytical SQL scripts (KPIs, Top 5 SKUs, Category x Region, Summaries)        |
+--------------------------------------------------------------------------------------------------+
|                                                |                                                 |
|                                                v                                                 |
|  [MODULE 4: Dimensional Modeling & Power BI Intelligence Engine]                                 |
|  Workbook: SPT.pbix | Star Schema Model: Fact_Sales (2,990 rows) <--- (N:1) ---> Dim_Calendar   |
|  DAX Measure Library: Total Sales, Net Profit, Margin %, Sales SPLY, YoY Growth %, 3-Page Canvas |
+--------------------------------------------------------------------------------------------------+
|                                                |                                                 |
|                                                v                                                 |
|  [MODULE 5: Interactive Web Application & Dashboard Deployment Engine]                           |
|  Script: app.py (Streamlit + Plotly) | Reactive state loop, @st.cache_data in-memory loading    |
|  Components: Dynamic Date Slider, Region/Category Slicers, 4 Interactive Charts, CSV Exporter    |
+--------------------------------------------------------------------------------------------------+
|                                                |                                                 |
|                                                v                                                 |
|  [MODULE 6: Publication-Grade Static Charting & Automated PDF Engine]                            |
|  Scripts: visuals/generate_charts.py & docs/generate_pdf.py                                      |
|  Artifacts: 4x 300 DPI Matplotlib PNGs, 106-page PDF Report, 13-page Master Appendix Compendium  |
+--------------------------------------------------------------------------------------------------+
```

### B.1 Module 1: Synthetic Data Generation & Controlled Anomaly Engine
* **Source Component**: `data/generate_sales_data.py`
* **Input Parameters**: Configuration parameters (Seed: 42, Row count: 3,000, Start date: `2023-01-01`, End date: `2024-12-31`).
* **Functional Operation**:
  1. Procedurally generates realistic commercial retail transaction records across 27 distinct product SKUs, 4 categories, and 4 geographic regions.
  2. Injects controlled data quality anomalies to mirror real-world point-of-sale defects:
     - Exact duplicate records (10 rows) simulating network re-submission retries.
     - Null/blank fields (10 rows) across Sales, Profit, Discount, Category, and Region.
     - Case mismatches (e.g., `technology`, `north`) and trailing whitespace (e.g., `'Furniture '`).
* **Output Deliverable**: `data/raw_sales_data.csv` (3,000 rows, 10 columns) and `data/DATA_QUALITY_NOTES.md`.

### B.2 Module 2: Data Cleansing, Hygiene & Transformation Engine
* **Source Component**: Excel Audit & Python Data Cleansing Workflow
* **Input**: `data/raw_sales_data.csv` (3,000 rows)
* **Functional Operation**:
  1. **Deduplication**: Audits primary key `Order_ID` and drops exactly 10 duplicate rows, yielding 2,990 unique transactions.
  2. **Deterministic Imputation**: Rather than inserting artificial column means, missing financial fields are mathematically re-derived:
     - Sales = Quantity * Base Price * (1 - Discount)
     - Profit = Sales - (Quantity * Wholesale Cost)
     - Discount = ((Qty * Price) - Sales) / (Qty * Price)
  3. **Categorical Normalization**: Applies `TRIM()` and `PROPER()` transformations to sanitize categories and regions into uniform Title Case.
* **Output Deliverable**: `sales_data_cleaning.csv` (2,990 clean, fully populated records).

### B.3 Module 3: Relational Database Staging & SQL Analytical Execution Engine
* **Source Component**: `sql/sales_analysis.db` and `sql/schema_and_queries.sql`
* **Input**: `sales_data_cleaning.csv`
* **Functional Operation**:
  1. **Schema Initialization**: Constructs table `sales_data` with strict type constraints (`INTEGER`, `REAL`, `DATE`, `VARCHAR`).
  2. **Indexing**: Creates B-Tree indexes on `Category`, `Region`, `Order_Date`, and `Product` to achieve O(log N) query performance.
  3. **Analytical Query Suite**:
     - *Query 1*: Aggregates high-level enterprise metrics ($450,978.56 sales, $157,745.23 profit, 34.98% margin).
     - *Query 2*: Ranks Top 5 revenue-generating products using `ORDER BY Total_Sales DESC LIMIT 5`.
     - *Query 3*: Computes multi-dimensional Category x Region cross-tabulation.
     - *Query 4*: Analyzes merchandise category volume versus profitability.
     - *Query 5*: Evaluates regional revenue and margin distribution.
* **Output Deliverables**: `sql/sales_analysis.db` and `sql/QUERY_RESULTS.md`.

### B.4 Module 4: Dimensional Modeling & Power BI Intelligence Engine
* **Source Component**: `SPT.pbix`
* **Input**: Cleaned transactional table staged from SQLite / CSV.
* **Functional Operation**:
  1. **Star Schema Architecture**: Decouples transactional facts into `Fact_Sales` and temporal dimensional attributes into `Dim_Calendar` (731 dates from 2023 to 2024).
  2. **Relationship**: Configures a 1-to-Many single-directional relationship: `Dim_Calendar[DateKey]` -> `Fact_Sales[Order_Date]`.
  3. **DAX Measure Library**: Authors explicit DAX measures for financial base values (`[Total Sales]`, `[Total Profit]`, `[Overall Margin %]`), transaction KPIs (`[Total Orders]`, `[AOV]`), and time intelligence (`[Sales YTD]`, `[Sales SPLY]`, `[YoY Growth %]`).
  4. **Canvas Design**: Implements a 3-page interactive layout:
     - *Page 1: Executive Overview* (Headline cards, 24-month trend, category donut).
     - *Page 2: Product & Category Deep-Dive* (Ranked bar charts, margin matrix).
     - *Page 3: Regional Commercial Diagnostics* (Geographic breakdown, customer frequency).
* **Output Deliverables**: `SPT.pbix` and `powerbi/README.md`.

### B.5 Module 5: Interactive Web Application & Dashboard Deployment Engine
* **Source Component**: `app.py`
* **Framework**: Streamlit 1.63 + Plotly Graph Objects + Pandas
* **Functional Operation**:
  1. **In-Memory Caching**: Leverages `@st.cache_data` to load `sales_data_cleaning.csv` once, ensuring sub-50ms reactive filtering upon user input.
  2. **Responsive Sidebar Controls**: Dynamically populates date sliders, region multi-select dropdowns, and category filters.
  3. **Visual Layout**:
     - 5 Top KPI metric tiles displaying dynamically recalculated Sales, Profit, Margin, Order Count, and AOV.
     - Monthly sales trajectory line chart with peak annotation.
     - Category revenue share donut chart with center KPI scorecard.
     - Top 5 products horizontal bar chart with margin labels.
     - Regional sales vs. profit clustered column chart.
  4. **Self-Service Data Export**: Embeds a collapsible raw data table with one-click CSV download capability.
* **Output Deliverable**: `app.py` runnable locally via `streamlit run app.py` and cloud-deployable on Streamlit Community Cloud.

### B.6 Module 6: Publication-Grade Static Charting & Automated PDF Engine
* **Source Components**: `visuals/generate_charts.py` and `docs/generate_pdf.py`
* **Functional Operation**:
  1. **Static Visual Generation**: Connects to `sql/sales_analysis.db` and utilizes Matplotlib to render four 300 DPI high-resolution PNG charts (`01_sales_trend.png`, `02_top_5_products.png`, `03_category_sales_donut.png`, `04_regional_performance.png`).
  2. **Automated PDF Compilation**: Compiles the markdown documentation into styled HTML and invokes headless Google Chrome / Microsoft Edge to produce:
     - Complete formal report (`SUMMER_TRAINING_REPORT.pdf`).
     - Standalone quick-reference compendium (`MASTER_APPENDIX.pdf`).
* **Output Deliverables**: `visuals/*.png`, `SUMMER_TRAINING_REPORT.pdf`, and `MASTER_APPENDIX.pdf`.
"""

def update_files():
    with open(REPORT_MD, "r", encoding="utf-8") as f:
        report = f.read()

    # Old TOC table chunk
    old_toc = """| Appendix A | Complete SQL Schema and Analytical Queries (`schema_and_queries.sql`) | 144 |
| Appendix B | Complete Power BI DAX Measures Reference Library | 148 |
| Appendix C | Interactive Streamlit Dashboard Source Code (`app.py`) | 151 |
| Appendix D | Automated Visualization Generator Source Code (`generate_charts.py`) | 156 |
| Appendix E | Raw Data Quality Defects Audit Log (`DATA_QUALITY_NOTES.md`) | 160 |
| Appendix F | Master Project Quick-Reference & Executive Compendium (`MASTER_APPENDIX.md`) | 163 |"""

    new_toc = """| Appendix A | Software and Tools Used | 142 |
| Appendix B | Project Modules & Architectural Breakdown | 145 |
| Appendix C | Complete SQL Schema and Analytical Queries (`schema_and_queries.sql`) | 149 |
| Appendix D | Complete Power BI DAX Measures Reference Library | 153 |
| Appendix E | Interactive Streamlit Dashboard Source Code (`app.py`) | 156 |
| Appendix F | Automated Visualization Generator Source Code (`generate_charts.py`) | 161 |
| Appendix G | Raw Data Quality Defects Audit Log (`DATA_QUALITY_NOTES.md`) | 165 |
| Appendix H | Master Project Quick-Reference & Executive Compendium (`MASTER_APPENDIX.md`) | 168 |"""

    if old_toc in report:
        report = report.replace(old_toc, new_toc)

    # Relabel old appendices
    report = report.replace("## Appendix F: Master Project Quick-Reference", "## Appendix H: Master Project Quick-Reference")
    report = report.replace("## Appendix E: Raw Data Quality Defects", "## Appendix G: Raw Data Quality Defects")
    report = report.replace("## Appendix D: Automated Visualization Generator", "## Appendix F: Automated Visualization Generator")
    report = report.replace("## Appendix C: Interactive Streamlit Dashboard", "## Appendix E: Interactive Streamlit Dashboard")
    report = report.replace("## Appendix B: Complete Power BI DAX Measures", "## Appendix D: Complete Power BI DAX Measures")
    report = report.replace("## Appendix A: Complete SQL Schema and Analytical Queries", "## Appendix C: Complete SQL Schema and Analytical Queries")

    appendices_marker = "# APPENDICES\n\n---\n\n"
    if appendices_marker in report and "## Appendix A: Software and Tools Used" not in report:
        insertion = appendices_marker + appendix_a_text + "\n\n---\n\n\\newpage\n\n" + appendix_b_text + "\n\n---\n\n\\newpage\n\n"
        report = report.replace(appendices_marker, insertion, 1)

    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write(report)
    with open(DOCS_REPORT_MD, "w", encoding="utf-8") as f:
        f.write(report)

    # Now update MASTER_APPENDIX.md
    with open(MASTER_MD, "r", encoding="utf-8") as f:
        master = f.read()

    # Check if Appendix A and B are in MASTER_APPENDIX
    if "## Appendix A: Software and Tools Used" not in master:
        # Insert Appendix A and B right before SECTION 3 or after SECTION 1
        sec1_marker = "# SECTION 1: ACADEMIC & INSTITUTIONAL ALIGNMENT MATRIX\n"
        sec2_marker = "# SECTION 2: END-TO-END ANALYTICS LIFECYCLE & PIPELINE\n"
        
        appendix_ab_block = f"""
---

# PART A: SOFTWARE AND TOOLS USED

{appendix_a_text.replace("## Appendix A: Software and Tools Used", "")}

---

# PART B: PROJECT MODULES & ARCHITECTURAL BREAKDOWN

{appendix_b_text.replace("## Appendix B: Project Modules & Architectural Breakdown", "")}
"""
        master = master.replace(sec2_marker, appendix_ab_block + "\n---\n\n" + sec2_marker)

        with open(MASTER_MD, "w", encoding="utf-8") as f:
            f.write(master)
        with open(DOCS_MASTER_MD, "w", encoding="utf-8") as f:
            f.write(master)

    print("Updated all reports and master appendices successfully!")

if __name__ == "__main__":
    update_files()
