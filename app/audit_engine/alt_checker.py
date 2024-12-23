from bs4 import BeautifulSoup

def check_alt_attributes(html_content):
    """
    Checks for missing alt attributes in <img> tags.
    Returns a list of issues for images without alt attributes.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all <img> tags missing the alt attribute
    images_without_alt = soup.find_all('img', alt=False)
    
    issues = []
    for img in images_without_alt:
        issues.append({
            'tag': str(img),
            'message': "Missing alt attribute for image accessibility."
        })
    
    return issues
