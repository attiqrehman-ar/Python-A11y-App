
from bs4 import BeautifulSoup


def check_link_text_clarity(html_content):
    """
    Checks for vague link text and suggests improvements. It now considers the presence of `aria-label`.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    issues = []
    links = soup.find_all('a')

    for link in links:
        # Check if aria-label is present, if not, look for the visible text
        visible_text = link.get_text(strip=True)
        aria_label = link.get('aria-label', '').strip()

        if not aria_label and not visible_text:
            issues.append({
                'tag': str(link),
                'message': "Link has neither visible text nor aria-label, making it unclear."
            })
        elif aria_label and len(aria_label) < 3:
            issues.append({
                'tag': str(link),
                'message': "aria-label is too vague or too short."
            })

    return issues
