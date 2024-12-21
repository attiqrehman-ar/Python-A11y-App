from app.audit_engine.alt_checker import check_alt_attributes
from app.audit_engine.aria_checker import check_aria_labels
from app.audit_engine.contrast_checker import check_color_contrast_in_html  # New import
from app.audit_engine.heading_checker import check_headings_structure
from app.audit_engine.link_checker import check_link_text_clarity
from app.utils.report_generator import generate_report

def main():
    # Load HTML content (for now, you can load from a file or string)
    with open('sample_page.html', 'r') as file:
        html_content = file.read()

    # Run checks
    alt_issues = check_alt_attributes(html_content)
    aria_issues = check_aria_labels(html_content)
    contrast_issues = check_color_contrast_in_html(html_content)  # Run the new check
    heading_issues = check_headings_structure(html_content)
    link_issues = check_link_text_clarity(html_content)
    # Generate the report
    report = ""
    if alt_issues:
        report += generate_report(alt_issues, "Alt Text Check")
    if aria_issues:
        report += generate_report(aria_issues, "ARIA Label Check")
    if contrast_issues:  # Add the color contrast issues to the report
        report += generate_report(contrast_issues, "Color Contrast Check")
    if heading_issues:
        report += generate_report(heading_issues, "Headings Structure Check")  # Added heading structure check report
    if link_issues:
        report += generate_report(link_issues, "Link Text Clarity Check")
    # If no issues, report that everything is fine
    if not alt_issues and not aria_issues and not contrast_issues and not heading_issues and not link_issues:
        report = "All checks passed! No issues found.\n"

    # Output the report
    print(report)

    # Optionally, save the report to a file
    with open('accessibility_report.txt', 'w') as report_file:
        report_file.write(report)

if __name__ == "__main__":
    main()
