# app/audit_engine/heading_checker.py

from bs4 import BeautifulSoup

def check_headings_structure(html_content):
    """
    Checks that the heading tags in the HTML content follow a proper order.
    Flags any skipped headings (e.g., from <h1> to <h3> without an <h2>).
    Returns a list of issues in the format:
    [
        {'message': 'Skipped heading <h2> after <h1>', 'tag': '<h3>Some skipped heading</h3>'}
    ]
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    issues = []
    last_heading_level = 0

    for heading in headings:
        level = int(heading.name[1])  # Extract the level from the heading tag (e.g., <h1> -> 1)
        
        if level > last_heading_level + 1:
            issues.append({
                'message': f"Skipped heading <h{last_heading_level + 1}> after <h{level}>",
                'tag': str(heading)
            })
        
        last_heading_level = level

    return issues
