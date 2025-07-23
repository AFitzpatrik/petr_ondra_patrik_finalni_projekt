from django import template
from viewer.models import Event

register = template.Library()

@register.filter
def event_count_for_city(city):
    return Event.objects.filter(location__city=city).count()

@register.filter
def sklonuj_udalost(pocet):
    try:
        pocet = int(pocet)
    except (ValueError, TypeError):
        return "událostí"

    if pocet == 1:
        return "událost"
    elif 2 <= pocet <= 4:
        return "události"
    else:
        return "událostí"
