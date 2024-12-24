# backend/app.py
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

from app.audit_engine.alt_checker import check_alt_attributes
from app.audit_engine.aria_checker import check_aria_labels
from app.audit_engine.heading_checker import check_headings_structure
from app.utils.report_generator import generate_report

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
CORS(app)

# Function to fetch HTML content from URL using Selenium
def fetch_html_from_url(url):
    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    html_content = driver.page_source
    driver.quit()
    return html_content

# Endpoint to check accessibility for a webpage URL
@app.route('/api/check-url-accessibility', methods=['POST'])
def api_check_url_accessibility():
    content = request.json
    url = content.get('url', '')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Fetch HTML content and perform checks
    try:
        html_content = fetch_html_from_url(url)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch HTML from URL: {str(e)}"}), 500

    # Perform accessibility checks
    results = {
        "alt_text": check_alt_attributes(html_content),
        "aria_labels": check_aria_labels(html_content),
        "heading_structure": check_headings_structure(html_content)
    }

    return jsonify(results)

# Generate PDF report from the results
@app.route('/api/generate-pdf-report', methods=['POST'])
def api_generate_pdf_report():
    content = request.json
    results = content.get('results', [])

    # Create a PDF in memory
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)

    y_position = 750  # Start at the top of the page
    c.drawString(100, y_position, "Accessibility Report")
    y_position -= 30

    for category, issues in results.items():
        c.drawString(100, y_position, f"{category.replace('_', ' ').title()}:")
        y_position -= 20

        if isinstance(issues, list) and issues:
            for issue in issues:
                c.drawString(100, y_position, f"- {issue['message']}")
                y_position -= 15

        y_position -= 10  # Space between categories

    c.showPage()
    c.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="accessibility_report.pdf", mimetype="application/pdf")

if __name__ == '__main__':
    app.run(debug=True)
