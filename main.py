import requests
from app.audit_engine.alt_checker import check_alt_attributes
from app.audit_engine.aria_checker import check_aria_labels
from app.audit_engine.contrast_checker import check_color_contrast_in_html
from app.audit_engine.heading_checker import check_headings_structure
from app.audit_engine.keyboard_navigation_checker import check_keyboard_navigation
from app.audit_engine.link_checker import check_link_text_clarity
from app.utils.report_generator import generate_report
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def fetch_html_from_url(url):
    """
    Fetches the HTML content of the webpage from the provided URL.
    """
    # Check if the URL includes a scheme (http or https)
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        print(f"Error fetching URL: Invalid URL '{url}': No scheme supplied. Perhaps you meant https://?")
        return None

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def main():
    # Get the URL from the user
    url = input("Enter the URL to check: ").strip()
    
    if not url:
        print("No URL provided.")
        return
    
    # Fetch the HTML content from the URL
    html_content = fetch_html_from_url(url)
    
    if html_content:
        # Run checks
        alt_issues = check_alt_attributes(html_content)
        aria_issues = check_aria_labels(html_content)
        contrast_issues = check_color_contrast_in_html(html_content)
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
