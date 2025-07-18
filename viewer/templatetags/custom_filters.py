from django import template

register = template.Library()

@register.filter
def sklonuj_udalost(pocet):
    if pocet == 1:
        return "událost"
    elif 2 <= pocet <= 4:
        return "události"
    else:
        return "událostí"