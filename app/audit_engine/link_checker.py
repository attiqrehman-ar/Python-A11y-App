from bs4 import BeautifulSoup

def check_link_text_clarity(html_content):
    """
    Check if link texts are descriptive.
    """
    issues = []
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all anchor tags
    links = soup.find_all('a')
    
    for link in links:
        link_text = link.get_text().strip()
        
        # Check for vague link texts
        if link_text.lower() in ["click here", "read more", "learn more", "more details"]:
            issues.append({
                'message': 'Vague link text.',
                'tag': str(link)
            })
    
    return issues
