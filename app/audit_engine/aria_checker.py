from bs4 import BeautifulSoup

def check_aria_labels(html_content):
    """
    Checks for missing aria-label attributes in interactive elements.
    Returns a list of elements missing aria-labels.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Check more interactive elements: buttons, links, divs with roles, etc.
    interactive_elements = soup.find_all(['button', 'a', 'input', 'div', 'span'], 
                                         attrs={'role': True})  # Elements with role attribute

    issues = []
    for element in interactive_elements:
        if not element.has_attr('aria-label'):
            issues.append({
                'tag': str(element),
                'message': "Missing aria-label attribute."
            })
    
    # Also check elements without a 'role' attribute, but are interactive
    non_role_elements = soup.find_all(['button', 'a', 'input'])
    for element in non_role_elements:
        if not element.has_attr('aria-label') and not element.has_attr('aria-labelledby'):
            issues.append({
                'tag': str(element),
                'message': "Missing aria-label attribute."
            })

    return issues

# Test the function with a sample HTML
if __name__ == "__main__":
    sample_html = """
   <html>
    <body>
        <button>Submit</button> <!-- Should trigger an issue -->
        <a href="#">Click me</a> <!-- Should trigger an issue -->
        <div role="button">No label</div> <!-- Should trigger an issue -->
        <span role="button" aria-label="Click to proceed">Go</span> <!-- Should NOT trigger an issue -->
        <input type="text" placeholder="Enter text"> <!-- Should NOT trigger an issue -->
        <a href="#" aria-label="Home">Home</a> <!-- Should NOT trigger an issue -->
    </body>
</html>
    """
    issues = check_aria_labels(sample_html)
    for issue in issues:
        print(f"Issue: {issue['message']}\nTag: {issue['tag']}")
