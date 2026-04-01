from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """
    Permet d'accéder à un dictionnaire avec une clé dans un template Django
    """
    return dictionary.get(key, None)

@register.filter
def add_opacity(hex_color, opacity):
    """
    Ajoute une opacité à une couleur hexadécimale
    """
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    
    # Convertir hex en RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    return f'rgba({r}, {g}, {b}, {opacity})'
