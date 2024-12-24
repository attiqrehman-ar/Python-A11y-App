from flask import Flask, jsonify, request
from flask_cors import CORS
from app.audit_engine.alt_checker import check_alt_attributes
from app.audit_engine.aria_checker import check_aria_labels
from app.audit_engine.contrast_checker import check_color_contrast_in_html
from app.audit_engine.heading_checker import check_headings_structure
from app.audit_engine.keyboard_navigation_checker import check_keyboard_navigation
from app.utils.report_generator import generate_report

app = Flask(__name__)
CORS(app)

# Example endpoint for alt text check
@app.route('/api/check-alt-text', methods=['POST'])
def api_check_alt_text():
    content = request.json
    html_content = content.get('html', '')
    result = check_alt_attributes(html_content)
    return jsonify(result)

# Example endpoint for ARIA label check
@app.route('/api/check-aria-labels', methods=['POST'])
def api_check_aria_labels():
    content = request.json
    html_content = content.get('html', '')
    result = check_aria_labels(html_content)
    return jsonify(result)

# Example endpoint for color contrast check
@app.route('/api/check-color-contrast', methods=['POST'])
def api_check_color_contrast():
    content = request.json
    html_content = content.get('html', '')
    result = check_color_contrast_in_html(html_content)
    return jsonify(result)

# Example endpoint for heading structure check
@app.route('/api/check-heading-structure', methods=['POST'])
def api_check_heading_structure():
    content = request.json
    html_content = content.get('html', '')
    result = check_headings_structure(html_content)
    return jsonify(result)

# Example endpoint for keyboard navigation check
@app.route('/api/check-keyboard-navigation', methods=['POST'])
def api_check_keyboard_navigation():
    content = request.json
    html_content = content.get('html', '')
    result = check_keyboard_navigation(html_content)
    return jsonify(result)

# Endpoint to generate report
@app.route('/api/generate-report', methods=['POST'])
def api_generate_report():
    content = request.json
    checks_results = content.get('results', [])
    report = generate_report(checks_results)
    return jsonify({"report": report})

if __name__ == '__main__':
    app.run(debug=True)
