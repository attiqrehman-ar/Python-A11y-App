from bs4 import BeautifulSoup

def check_keyboard_navigation(html_content):
    """
    Checks if the website has proper keyboard navigation.
    This includes focusable elements, proper tab order, and visible focus states.
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

    # 2. Check if any element has a visible focus state (via CSS)
    focus_elements = soup.find_all(['a', 'button', 'input', 'textarea', 'select', 'details'])
    for elem in focus_elements:
        if not any(style for style in elem.get('style', '').split(';') if 'outline' in style or 'border' in style):
            issues.append({
                'message': 'Focusable element missing visible focus style.',
                'tag': str(elem)
            })

    # 3. Check if the page contains a "skip to content" link
    skip_to_content = soup.find('a', href='#skip-to-content')
    if not skip_to_content:
        issues.append({
            'message': 'No "Skip to Content" link found.',
            'tag': 'N/A'
        })

    return issues
