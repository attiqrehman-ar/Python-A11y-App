from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import re
from bs4 import BeautifulSoup

from app.audit_engine.alt_checker import check_alt_attributes
from app.audit_engine.aria_checker import check_aria_labels
from app.audit_engine.heading_checker import check_headings_structure

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
    options.headless = True  # Run in headless mode (no browser window)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    html_content = driver.page_source
    driver.quit()
    return html_content

# Function to clean up HTML elements
def clean_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup

# Function to process alt text issues
def process_alt_text(html_content):
    soup = clean_html(html_content)
    issues = []
    images = soup.find_all('img')
    for img in images:
        alt = img.get('alt', None)
        if not alt:
            issues.append({
                "tag": "img",
                "location": str(img)
            })
    return issues

# Function to process ARIA labels issues
def process_aria_labels(html_content):
    soup = clean_html(html_content)
    issues = []
    # Look for elements with ARIA attributes
    elements_with_aria = soup.find_all(attrs={'aria-label': True})
    for element in elements_with_aria:
        if not element.get('aria-label'):
            issues.append({
                "tag": str(element),
                "location": str(element)
            })
    return issues

# Function to process heading structure issues
def process_heading_structure(html_content):
    soup = clean_html(html_content)
    issues = []
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for i in range(1, len(headings)):
        prev_heading = headings[i-1]
        current_heading = headings[i]
        # Check if there is a skipped heading
        if int(current_heading.name[1]) > int(prev_heading.name[1]) + 1:
            issues.append({
                "message": f"Skipped heading {prev_heading.name} after {current_heading.name}",
                "location": str(current_heading)
            })
    return issues

# Endpoint to check accessibility for a webpage URL
@app.route('/api/check-url-accessibility', methods=['POST'])
def api_check_url_accessibility():
    content = request.json
    url = content.get('url', '')  # Get URL from the request

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        html_content = fetch_html_from_url(url)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch HTML from URL: {str(e)}"}), 500

    # Run accessibility checks
    alt_text_results = process_alt_text(html_content)
    aria_labels_results = process_aria_labels(html_content)
    heading_structure_results = process_heading_structure(html_content)

    results = {
        "alt_text": alt_text_results,
        "aria_labels": aria_labels_results,
        "heading_structure": heading_structure_results
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

    # Check for Alt Text Issues
    if results.get('alt_text'):
        c.drawString(100, y_position, "Alt Text Issues:")
        y_position -= 20
        for issue in results['alt_text']:
            c.drawString(100, y_position, f"- Missing alt attribute for {issue['tag']} at {issue['location']}")
            y_position -= 15
        y_position -= 10  # Space between categories

    # Check for ARIA Labels Issues
    if results.get('aria_labels'):
        c.drawString(100, y_position, "ARIA Labels Issues:")
        y_position -= 20
        for issue in results['aria_labels']:
            c.drawString(100, y_position, f"- ARIA label missing for {issue['tag']} at {issue['location']}")
            y_position -= 15
        y_position -= 10  # Space between categories

    # Check for Heading Structure Issues
    if results.get('heading_structure'):
        c.drawString(100, y_position, "Heading Structure Issues:")
        y_position -= 20
        for issue in results['heading_structure']:
            c.drawString(100, y_position, f"- Skipped heading: {issue['message']} at {issue['location']}")
            y_position -= 15
        y_position -= 10  # Space between categories

    c.showPage()
    c.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="accessibility_report.pdf", mimetype="application/pdf")

if __name__ == '__main__':
    app.run(debug=True)
