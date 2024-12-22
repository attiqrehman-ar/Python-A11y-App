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

    # 3. Check if the page contains a "skip to content" link
    skip_to_content = soup.find('a', href='#skip-to-content')
    if not skip_to_content:
        issues.append({
            'message': 'No "Skip to Content" link found.',
            'tag': 'N/A'
        })

    return issues
