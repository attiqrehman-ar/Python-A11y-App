from bs4 import BeautifulSoup

def check_alt_attributes(html_content):
    """
    Checks for missing alt attributes in <img> tags.
    Returns a list of <img> tags without alt attributes.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    images_without_alt = soup.find_all('img', alt=False)
    
    issues = []
    for img in images_without_alt:
        issues.append({
            'tag': str(img),
            'message': "Missing alt attribute."
        })
    
    return issues

# Test the function with a sample HTML
if __name__ == "__main__":
    sample_html = """
    <html>
        <body>
            <img src="image1.jpg">
            <img src="image2.jpg" alt="A sample image">
            <img src="image3.jpg">
        </body>
    </html>
    """
    issues = check_alt_attributes(sample_html)
    for issue in issues:
        print(f"Issue: {issue['message']}\nTag: {issue['tag']}")
