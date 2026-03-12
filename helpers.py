def rs(value):
    """Format value as Rupee."""
    return f"₹{value:,}"

COLOR_MAP = {
    "black": "#000000",
    "maroon": "#800000",
    "apricot": "#F5F5DC",
    "ivory": "#FFFFF0",
    "sky": "#A2B5CD",
    "navy": "#1B2237",
    "lime green": "#B7CE63",
    "yellow": "#FFFD74",
    "olive green": "#808000",
    "beige": "#FFFDD0",
    "light green": "#D1FFBD",
    "pink": "#FF1493",
    "denim blue": "#2243B6",
    "grey": "#808080",
    "white": "#ffffff",
    "dark blue": "#00008B",
    "light fade blue": "#658CBB",
    "sky blue": "#87CEEB",
    "purple": "#800080",
    "off-white": "#FAF9F6"
}

def get_hex_color(color_name):
    return COLOR_MAP.get(color_name.lower(), "#000000")