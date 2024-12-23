from bs4 import BeautifulSoup

def check_aria_labels(html_content):
    """
    Checks for missing aria-label attributes on specific anchor elements:
    - Links opening in a new tab (target="_blank").
    - Links with generic text like "Read more", "Learn more", or "Click here".
    Returns a list of issues.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    issues = []

    # Define generic text patterns to flag
    generic_text_patterns = ['read more', 'learn more', 'click here']

    # Find all anchor tags
    anchor_tags = soup.find_all('a')

    for anchor in anchor_tags:
        text_content = anchor.get_text(strip=True).lower()  # Get text and normalize
        target_blank = anchor.get('target') == '_blank'

        # Check if the link matches the criteria
        if (target_blank or any(pattern in text_content for pattern in generic_text_patterns)):
            if not anchor.has_attr('aria-label') and not anchor.has_attr('aria-labelledby'):
                issues.append({
                    'tag': str(anchor),
                    'message': 'Anchor missing aria-label or aria-labelledby for accessibility.'
                })

    return issues
