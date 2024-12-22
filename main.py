import requests
from bs4 import BeautifulSoup
from app.audit_engine.alt_checker import check_alt_attributes
from app.audit_engine.aria_checker import check_aria_labels
from app.audit_engine.color_contrast_checker import check_color_contrast
from app.audit_engine.headings_structure_checker import check_headings_structure
from app.audit_engine.link_clarity_checker import check_link_text_clarity
from app.audit_engine.keyboard_navigation_checker import check_keyboard_navigation
from app.utils.report_generator import generate_report

def fetch_html_from_url(url):
    """
    Fetches the HTML content from a given URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def main():
    url = input("Enter the URL of the website to audit: ")

    # Fetch HTML content from the URL
    html_content = fetch_html_from_url(url)
    if not html_content:
        return

    # Run accessibility checks
    alt_issues = check_alt_attributes(html_content)
    aria_issues = check_aria_labels(html_content)
    contrast_issues = check_color_contrast(html_content)
    heading_issues = check_headings_structure(html_content)
    link_issues = check_link_text_clarity(html_content)
    keyboard_issues = check_keyboard_navigation(html_content)

    # Generate the report
    report = ""
    if alt_issues:
        report += generate_report(alt_issues, "Alt Text Check")
    if aria_issues:
        report += generate_report(aria_issues, "ARIA Label Check")
    if contrast_issues:
        report += generate_report(contrast_issues, "Color Contrast Check")
    if heading_issues:
        report += generate_report(heading_issues, "Headings Structure Check")
    if link_issues:
        report += generate_report(link_issues, "Link Text Clarity Check")
    if keyboard_issues:
        report += generate_report(keyboard_issues, "Keyboard Navigation Check")
    
    # If no issues, report that everything is fine
    if not any([alt_issues, aria_issues, contrast_issues, heading_issues, link_issues, keyboard_issues]):
        report = "All checks passed! No issues found.\n"

    # Output the report
    print(report)

    # Optionally, save the report to a file
    with open('accessibility_report.txt', 'w') as report_file:
        report_file.write(report)

if __name__ == "__main__":
    main()
