def generate_report(issues, rule_name):
    """
    Generates a simple text report for the issues found in a webpage.
    """
    report = f"Accessibility Report - {rule_name}\n"
    report += "=" * 50 + "\n"
    
    if issues:
        for issue in issues:
            report += f"Issue: {issue['message']}\nTag: {issue['tag']}\n\n"
    else:
        report += "No issues found!\n"
    
    report += "=" * 50 + "\n"
    return report

# Example of how to use the function:
if __name__ == "__main__":
    sample_issues = [
        {'message': 'Missing alt attribute.', 'tag': '<img src="image1.jpg">'},
        {'message': 'Missing aria-label attribute.', 'tag': '<button>Submit</button>'}
    ]
    report = generate_report(sample_issues, 'Accessibility Checks')
    print(report)
