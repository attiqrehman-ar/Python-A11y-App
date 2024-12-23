from bs4 import BeautifulSoup
import re

def calculate_luminance(color):
    """Calculate luminance for color contrast check."""
    if color.startswith('#'):
        r, g, b = [int(color[i:i+2], 16) for i in (1, 3, 5)]
    elif color.startswith('rgb'):
        r, g, b = map(int, re.findall(r'\d+', color))
    else:
        return 0  # Unknown color format
    
    r, g, b = [x / 255.0 for x in (r, g, b)]
    
    for i in range(3):
        if r <= 0.03928:
            r /= 12.92
        else:
            r = ((r + 0.055) / 1.055) ** 2.4
    
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return luminance

def calculate_contrast_ratio(color1, color2):
    """Calculate the contrast ratio between two colors."""
    luminance1 = calculate_luminance(color1)
    luminance2 = calculate_luminance(color2)
    
    if luminance1 > luminance2:
        contrast = (luminance1 + 0.05) / (luminance2 + 0.05)
    else:
        contrast = (luminance2 + 0.05) / (luminance1 + 0.05)
    
    return contrast

def check_color_contrast_in_html(html_content):
    """Check color contrast in HTML content and pinpoint issues."""
    soup = BeautifulSoup(html_content, 'html.parser')

    issues = []
    elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'a', 'button', 'li'])

    for element in elements:
        text = element.get_text(strip=True)
        
        if not text:
            continue
        
        # Get color and background color from the element's style attribute
        color = element.get('style', '').split('color:')[-1].split(';')[0].strip()
        background = element.get('style', '').split('background-color:')[-1].split(';')[0].strip()
        
        if color and background:
            contrast = calculate_contrast_ratio(color, background)
            
            # If contrast is below the required level, add the issue with details
            if contrast < 4.5:
                issues.append({
                    'message': f'Poor color contrast. Contrast ratio: {contrast:.2f}',
                    'tag': str(element),
                    'color': color,
                    'background': background,
                    'contrast_ratio': contrast
                })

    return issues
