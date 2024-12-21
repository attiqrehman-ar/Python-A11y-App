import re

def check_vague_link_text(html_content):
    """
    Check for links with vague or unclear text content.
    Flags links with generic text like 'Click here', 'Read more', etc.
    """
    issues = []
    # Regex to find all anchor tags
    links = re.findall(r'<a[^>]*>(.*?)</a>', html_content)
    
    vague_texts = ['click here', 'read more', 'learn more', 'more details', 'click me']
    
    for link in links:
        # Check if the link text matches any of the vague texts (case insensitive)
        for vague_text in vague_texts:
            if re.search(r'\b' + re.escape(vague_text) + r'\b', link, re.IGNORECASE):
                issues.append({
                    'message': f'Vague link text. Consider more descriptive text.',
                    'tag': f'<a>{link}</a>'
                })
                
    return issues
