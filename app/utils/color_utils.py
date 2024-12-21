# app/utils/color_utils.py

import webcolors

def get_rgb_from_color(color):
    """Converts color name to RGB."""
    try:
        return webcolors.name_to_rgb(color)
    except ValueError:
        pass
    return None

def luminance(rgb):
    """Calculates the relative luminance of a color (0 to 1 scale)."""
    r, g, b = [x / 255.0 for x in rgb]
    a = [r, g, b]
    
    for i in range(3):
        if a[i] <= 0.03928:
            a[i] /= 12.92
        else:
            a[i] = ((a[i] + 0.055) / 1.055) ** 2.4
    
    return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2]

def contrast_ratio(color1, color2):
    """Calculate the contrast ratio between two colors."""
    luminance1 = luminance(get_rgb_from_color(color1))
    luminance2 = luminance(get_rgb_from_color(color2))

    if luminance1 > luminance2:
        return (luminance1 + 0.05) / (luminance2 + 0.05)
    else:
        return (luminance2 + 0.05) / (luminance1 + 0.05)

def check_color_contrast(text_color, background_color):
    """Check if the contrast ratio between text and background is sufficient."""
    ratio = contrast_ratio(text_color, background_color)
    if ratio < 4.5:
        return f"Issue: Poor color contrast. Contrast ratio: {ratio:.2f}"
    return "Color contrast is sufficient."
