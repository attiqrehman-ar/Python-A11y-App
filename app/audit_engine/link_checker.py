from bs4 import BeautifulSoup

def check_link_text_clarity(html_content):
    """
    Checks if the website has links with clear, descriptive text.
    Ignores links that contain images with alt attributes describing the link.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    issues = []

    # Find all anchor tags
    links = soup.find_all('a')

    for link in links:
        # Skip links with images having alt text
        img = link.find('img')
        if img and img.get('alt'):  # If there's an image with alt text
            continue  # Don't flag this link, as the image's alt text describes the link

        # If no visible text and no aria-label, flag the link as vague
        if not link.get_text(strip=True) and not link.get('aria-label'):
            issues.append({
                'message': 'Link has neither visible text nor aria-label, making it unclear.',
                'tag': str(link)
            })

    return issues
