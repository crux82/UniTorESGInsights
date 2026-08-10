import matplotlib.colors as mcolors

BASE_COLORS = {
    "SA": "#4C78A8",  
    "17 SDG Alignment": "#009DDA",  
    "GRI Topic Alignment": "#1158A6",  
    "Informative & Non-Informative/Vague Sustainability Text Identification": "#F2C94C",  
    "Qualitative & Quantitative Sustainability Text Identification": "#F28E2B",  
    "High Potential Greenwashing Detection": "#4D4D4D", 
    "Climate Alignment": "#06402B", 
    "GRI Climate Alignment": "#00956D", 
    "GRI Climate Action (SDG13) Alignment": "#4C78A8", 
    "Climate Action (SDG13) Alignment": "#407F46" 
}

def get_shades(base_color, n):
    rgb = mcolors.to_rgb(base_color)
    shades = []

    for i in range(n):
        alpha = 0.3 + (i / max(n - 1, 1)) * 0.7  # transparent → solid
        
        r = int(rgb[0] * 255)
        g = int(rgb[1] * 255)
        b = int(rgb[2] * 255)

        shades.append(f"rgba({r},{g},{b},{alpha})") 

    return shades