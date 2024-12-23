from bs4 import BeautifulSoup

def check_keyboard_navigation(html_content):
    """
    Checks if the website has proper keyboard navigation.
    This includes focusable elements and the presence of a "skip to content" link.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    issues = []

    # 1. Check if there are focusable elements
    focusable_elements = soup.find_all(['a', 'button', 'input', 'textarea', 'select', 'details', '[tabindex]'])
    
    if not focusable_elements:
        issues.append({
            'message': 'No focusable elements found.',
            'tag': 'N/A'
        })
    elif len(focusable_elements) > 50:  # Check if there are a lot of focusable elements
        issues.append({
            'message': 'There are a large number of focusable elements, please check manually.',
            'tag': 'N/A'
        })

    # 2. Check if the page contains a "skip to content" link
    skip_to_content = soup.find('a', href=True)
    skip_to_content_found = False
    
    if skip_to_content:
        # Look for a "Skip to Content" link with appropriate text and href
        if ('skip' in skip_to_content.get_text().lower() and
            ('content' in skip_to_content.get_text().lower() or 'main' in skip_to_content.get_text().lower())):
            if not skip_to_content['href'].startswith('#') or skip_to_content['href'][1:] not in [id.lower() for id in ['main', 'content']]:
                issues.append({
                    'message': 'Skip to Content link found, but href does not point to main content.',
                    'tag': str(skip_to_content)
                })
            skip_to_content_found = True
    
    if not skip_to_content_found:
        issues.append({
            'message': 'No "Skip to Content" link found.',
            'tag': 'N/A'
        })

    return issues
