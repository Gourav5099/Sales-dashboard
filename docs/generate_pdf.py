import base64
import os
import re
import subprocess
import time
import markdown

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORT_MD_PATH = os.path.join(PROJECT_ROOT, "documentation", "SUMMER_TRAINING_REPORT.md")
VISUALS_DIR = os.path.join(PROJECT_ROOT, "visuals")
HTML_OUTPUT_PATH = os.path.join(PROJECT_ROOT, "documentation", "SUMMER_TRAINING_REPORT.html")
PDF_OUTPUT_DOCS = os.path.join(PROJECT_ROOT, "docs", "SUMMER_TRAINING_REPORT.pdf")
PDF_OUTPUT_DOC = os.path.join(PROJECT_ROOT, "documentation", "SUMMER_TRAINING_REPORT.pdf")
PDF_OUTPUT_ROOT = os.path.join(PROJECT_ROOT, "SUMMER_TRAINING_REPORT.pdf")

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]

def get_image_base64(filename):
    filepath = os.path.join(VISUALS_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    return None

def build_html_document(md_text):
    # Process mermaid blocks
    def replace_mermaid(match):
        code = match.group(1).strip()
        return f'<div class="mermaid-container"><div class="mermaid">\n{code}\n</div></div>'
    
    # Replace ```mermaid ... ``` with <div class="mermaid">...</div>
    processed_md = re.sub(r"```mermaid\s*\n(.*?)\n```", replace_mermaid, md_text, flags=re.DOTALL)
    
    # Replace \newpage with <div class="page-break"></div>
    processed_md = processed_md.replace(r"\newpage", '<div class="page-break"></div>')
    
    # Replace each Chapter 1..11 and Bibliography / Appendices with a page-break before it
    chapter_pattern = r"(^# (?:CHAPTER \d+|TABLE OF CONTENTS|PRELIMINARY PAGES|BIBLIOGRAPHY|APPENDICES|APPENDIX [A-F]).*?$)"
    processed_md = re.sub(chapter_pattern, r'<div class="page-break"></div>\n\n\1', processed_md, flags=re.MULTILINE)
    
    # Insert visual images where relevant figures are discussed in Chapter 7
    img_sales_trend = get_image_base64("01_sales_trend.png")
    img_top5 = get_image_base64("02_top_5_products.png")
    img_donut = get_image_base64("03_category_sales_donut.png")
    img_regional = get_image_base64("04_regional_performance.png")
    
    if img_sales_trend:
        fig_markup = f'\n\n<div class="figure-card"><img src="{img_sales_trend}" alt="Monthly Gross Sales and Profit Trend" /><p class="figure-caption"><strong>Figure 7.2:</strong> Monthly Gross Sales & Net Profit Performance Trend (2023–2024)</p></div>\n\n'
        processed_md = processed_md.replace("### Query 2: Top 5 Products by Revenue Contribution", fig_markup + "### Query 2: Top 5 Products by Revenue Contribution")
        
    if img_donut:
        fig_markup = f'\n\n<div class="figure-card"><img src="{img_donut}" alt="Category Revenue and Margin Donut" /><p class="figure-caption"><strong>Figure 7.4:</strong> Merchandise Category Revenue Contribution & Profit Margins</p></div>\n\n'
        processed_md = processed_md.replace("### Analytical Diagnosis:", fig_markup + "### Analytical Diagnosis:")
        
    if img_top5:
        fig_markup = f'\n\n<div class="figure-card"><img src="{img_top5}" alt="Top 5 Products Bar Chart" /><p class="figure-caption"><strong>Figure 7.3:</strong> Top 5 Revenue-Generating Products Leaderboard & Margin Comparison</p></div>\n\n'
        processed_md = processed_md.replace("### Diagnostic Product Observations:", fig_markup + "### Diagnostic Product Observations:")
        
    if img_regional:
        fig_markup = f'\n\n<div class="figure-card"><img src="{img_regional}" alt="Regional Performance Bar Chart" /><p class="figure-caption"><strong>Figure 7.5:</strong> Regional Commercial Breakdown: Gross Sales vs. Net Profit</p></div>\n\n'
        processed_md = processed_md.replace("### Diagnostic Regional Observations:", fig_markup + "### Diagnostic Regional Observations:")

    # Convert Markdown to HTML
    html_body = markdown.markdown(
        processed_md,
        extensions=[
            "extra",
            "toc",
            "sane_lists"
        ]
    )
    
    # Custom CSS for high-end academic styling
    css = """
    @page {
        size: A4 portrait;
        margin: 24mm 18mm 24mm 18mm;
    }
    
    @media print {
        .page-break {
            page-break-before: always;
            break-before: page;
        }
        .header {
            position: fixed;
            top: -18mm;
            left: 0;
            right: 0;
            height: 12mm;
            text-align: right;
            font-size: 7.5pt;
            color: #7F8C8D;
            border-bottom: 0.5pt solid #BDC3C7;
            padding-bottom: 2mm;
            font-family: 'Segoe UI', Arial, sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .footer {
            position: fixed;
            bottom: -18mm;
            left: 0;
            right: 0;
            height: 12mm;
            display: flex;
            justify-content: space-between;
            font-size: 7.5pt;
            color: #7F8C8D;
            border-top: 0.5pt solid #BDC3C7;
            padding-top: 2mm;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        tr {
            page-break-inside: avoid;
        }
        pre, blockquote, .figure-card {
            page-break-inside: avoid;
        }
        h1, h2, h3, h4 {
            page-break-after: avoid;
            break-after: avoid;
        }
    }
    
    * {
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Georgia', 'Helvetica Neue', Arial, sans-serif;
        font-size: 10pt;
        line-height: 1.55;
        color: #2C3E50;
        margin: 0;
        padding: 0;
        text-rendering: optimizeLegibility;
    }
    
    p {
        margin: 0 0 10pt 0;
        text-align: justify;
        text-justify: inter-word;
    }
    
    h1 {
        font-size: 20pt;
        font-weight: 700;
        color: #1F4E79;
        border-bottom: 2pt solid #1F4E79;
        padding-bottom: 4pt;
        margin-top: 18pt;
        margin-bottom: 12pt;
        letter-spacing: -0.3px;
    }
    
    h2 {
        font-size: 14pt;
        font-weight: 600;
        color: #2E75B6;
        border-bottom: 1pt solid #D6EAF8;
        padding-bottom: 3pt;
        margin-top: 14pt;
        margin-bottom: 8pt;
    }
    
    h3 {
        font-size: 11.5pt;
        font-weight: 600;
        color: #1B4F72;
        margin-top: 12pt;
        margin-bottom: 6pt;
    }
    
    h4 {
        font-size: 10.5pt;
        font-weight: 600;
        color: #2C3E50;
        margin-top: 10pt;
        margin-bottom: 4pt;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 12pt 0;
        font-size: 8.5pt;
        page-break-inside: auto;
    }
    
    thead th {
        background-color: #1F4E79;
        color: #FFFFFF;
        font-weight: 600;
        text-align: left;
        padding: 6pt 8pt;
        border: 1pt solid #1B4F72;
        letter-spacing: 0.2px;
    }
    
    tbody td {
        padding: 5pt 8pt;
        border: 0.5pt solid #D5DBDB;
        vertical-align: top;
    }
    
    tbody tr:nth-child(even) {
        background-color: #F8F9FA;
    }
    
    code {
        font-family: 'Cascadia Code', 'Consolas', 'Courier New', monospace;
        font-size: 8.5pt;
        background-color: #F2F4F4;
        color: #900C3F;
        padding: 1.5pt 4pt;
        border-radius: 3pt;
        border: 0.5pt solid #E5E7E9;
    }
    
    pre {
        background-color: #F8F9F9;
        border: 1pt solid #BDC3C7;
        border-left: 3.5pt solid #1F4E79;
        border-radius: 3pt;
        padding: 8pt 10pt;
        overflow-x: auto;
        margin: 10pt 0;
        font-size: 8pt;
        line-height: 1.4;
        page-break-inside: avoid;
    }
    
    pre code {
        background: transparent;
        border: none;
        padding: 0;
        color: #2C3E50;
        font-size: 8pt;
    }
    
    blockquote {
        margin: 10pt 0;
        padding: 8pt 12pt;
        background-color: #EBF5FB;
        border-left: 3.5pt solid #2980B9;
        border-radius: 0 4pt 4pt 0;
        font-style: italic;
        color: #1A5276;
    }
    
    blockquote p {
        margin: 0;
    }
    
    ul, ol {
        margin: 0 0 10pt 0;
        padding-left: 20pt;
    }
    
    li {
        margin-bottom: 3.5pt;
    }
    
    hr {
        border: 0;
        height: 1pt;
        background-color: #BDC3C7;
        margin: 14pt 0;
    }
    
    .figure-card {
        text-align: center;
        margin: 14pt auto;
        padding: 8pt;
        border: 0.5pt solid #D5DBDB;
        border-radius: 4pt;
        background-color: #FAFAFA;
        max-width: 95%;
        page-break-inside: avoid;
    }
    
    .figure-card img {
        max-width: 100%;
        height: auto;
        border-radius: 3pt;
        display: block;
        margin: 0 auto;
    }
    
    .figure-caption {
        font-size: 8.5pt;
        font-style: italic;
        color: #566573;
        margin-top: 6pt;
        margin-bottom: 0;
        text-align: center;
    }
    
    .mermaid-container {
        text-align: center;
        margin: 12pt auto;
        background-color: #FFFFFF;
        padding: 6pt;
        border: 0.5pt solid #E5E7E9;
        border-radius: 4pt;
        page-break-inside: avoid;
    }
    
    /* Cover Page Formatting */
    .cover-page {
        text-align: center;
        padding: 30pt 20pt;
        border: 2.5pt double #1F4E79;
        min-height: 900pt;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    """
    
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Summer Training Report: Sales & Business Performance Analysis</title>
    <style>
{css}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            mermaid.initialize({{
                startOnLoad: true,
                theme: 'default',
                flowchart: {{ useMaxWidth: true, htmlLabels: true, curve: 'basis' }},
                securityLevel: 'loose'
            }});
        }});
    </script>
</head>
<body>
    <div class="header">Sales & Business Performance Analysis — Summer Training Report</div>
    <div class="footer">
        <span>Department of Computer Science & Engineering | Data Analytics Specialization</span>
        <span>Candidate: Gourav</span>
    </div>

{html_body}

</body>
</html>
"""
    return full_html

def convert_to_pdf():
    print(f"Reading {REPORT_MD_PATH}...")
    with open(REPORT_MD_PATH, "r", encoding="utf-8") as f:
        md_content = f.read()

    print("Building HTML document with academic styling, embedded high-res charts, and Mermaid...")
    html_content = build_html_document(md_content)

    with open(HTML_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Saved styled HTML to {HTML_OUTPUT_PATH} ({len(html_content)} bytes)")

    # Find Chrome or Edge
    browser_exe = None
    for p in CHROME_PATHS:
        if os.path.exists(p):
            browser_exe = p
            break

    if not browser_exe:
        raise RuntimeError("Neither Google Chrome nor Microsoft Edge was found on this system.")

    print(f"Using browser executable: {browser_exe}")
    print(f"Converting HTML to PDF via headless Chromium print engine...")

    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--generate-pdf-document-outline",
        "--virtual-time-budget=8000",
        f"--print-to-pdf={PDF_OUTPUT_DOC}",
        HTML_OUTPUT_PATH
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Subprocess stderr:", result.stderr)
        raise RuntimeError(f"Browser print-to-pdf failed with exit code {result.returncode}")

    # Verify file was generated
    if os.path.exists(PDF_OUTPUT_DOC):
        size = os.path.getsize(PDF_OUTPUT_DOC)
        print(f"Successfully generated {PDF_OUTPUT_DOC} (Size: {size:,} bytes)")
        
        # Copy to docs/ and workspace root
        import shutil
        shutil.copyfile(PDF_OUTPUT_DOC, PDF_OUTPUT_DOCS)
        shutil.copyfile(PDF_OUTPUT_DOC, PDF_OUTPUT_ROOT)
        print(f"Mirrored PDF to {PDF_OUTPUT_DOCS}")
        print(f"Mirrored PDF to {PDF_OUTPUT_ROOT}")
        
        # Count pages
        with open(PDF_OUTPUT_DOC, "rb") as f:
            raw_pdf = f.read()
            pages = len(re.findall(rb"/Type\s*/Page\b", raw_pdf))
            print(f"Total Pages in Generated PDF: {pages} pages")
            
        return pages, size
    else:
        raise FileNotFoundError(f"PDF file was not found at {PDF_OUTPUT_DOC}")

def convert_master_appendix_to_pdf():
    appendix_md_path = os.path.join(PROJECT_ROOT, "documentation", "MASTER_APPENDIX.md")
    appendix_html_path = os.path.join(PROJECT_ROOT, "documentation", "MASTER_APPENDIX.html")
    appendix_pdf_doc = os.path.join(PROJECT_ROOT, "documentation", "MASTER_APPENDIX.pdf")
    appendix_pdf_docs = os.path.join(PROJECT_ROOT, "docs", "MASTER_APPENDIX.pdf")
    appendix_pdf_root = os.path.join(PROJECT_ROOT, "MASTER_APPENDIX.pdf")

    print(f"\nReading {appendix_md_path}...")
    with open(appendix_md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = build_html_document(md_content)
    with open(appendix_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Copy html to docs
    import shutil
    shutil.copyfile(appendix_html_path, os.path.join(PROJECT_ROOT, "docs", "MASTER_APPENDIX.html"))

    browser_exe = None
    for p in CHROME_PATHS:
        if os.path.exists(p):
            browser_exe = p
            break

    if not browser_exe:
        raise RuntimeError("Browser not found.")

    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--generate-pdf-document-outline",
        "--virtual-time-budget=5000",
        f"--print-to-pdf={appendix_pdf_doc}",
        appendix_html_path
    ]

    subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(appendix_pdf_doc):
        shutil.copyfile(appendix_pdf_doc, appendix_pdf_docs)
        shutil.copyfile(appendix_pdf_doc, appendix_pdf_root)
        with open(appendix_pdf_doc, "rb") as f:
            pages = len(re.findall(rb"/Type\s*/Page\b", f.read()))
        size = os.path.getsize(appendix_pdf_doc)
        print(f"Successfully generated MASTER_APPENDIX.pdf ({pages} pages, {size:,} bytes)")
        return pages, size

if __name__ == "__main__":
    convert_to_pdf()
    convert_master_appendix_to_pdf()

