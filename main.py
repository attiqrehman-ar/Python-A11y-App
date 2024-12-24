from flask import Flask, jsonify, request
from flask_cors import CORS
from app.audit_engine.alt_checker import check_alt_attributes
from app.audit_engine.aria_checker import check_aria_labels
from app.audit_engine.contrast_checker import check_color_contrast_in_html
from app.audit_engine.heading_checker import check_headings_structure
from app.audit_engine.keyboard_navigation_checker import check_keyboard_navigation
from app.utils.report_generator import generate_report

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
CORS(app)

# Helper function to fetch HTML content from URL using Selenium
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

# Example endpoint to check accessibility for a webpage URL
@app.route('/api/check-url-accessibility', methods=['POST'])
def api_check_url_accessibility():
    content = request.json
    url = content.get('url', '')
    
    # Fetch the HTML content of the page
    html_content = fetch_html_from_url(url)
    
    # Run checks on the fetched HTML content
    results = {
        "alt_text": check_alt_attributes(html_content),
        "aria_labels": check_aria_labels(html_content),
        "color_contrast": check_color_contrast_in_html(html_content),
        "heading_structure": check_headings_structure(html_content),
        "keyboard_navigation": check_keyboard_navigation(html_content),
    }
    
    return jsonify(results)

# Endpoint to generate report
@app.route('/api/generate-report', methods=['POST'])
def api_generate_report():
    content = request.json
    checks_results = content.get('results', [])
    report = generate_report(checks_results)
    return jsonify({"report": report})

if __name__ == '__main__':
    app.run(debug=True)
