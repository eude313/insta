from django import template
from django.utils.timesince import timesince

register = template.Library()
@register.filter
def shorten_time_since(value):
    """
    Shortens the time since the given value (usually a datetime) to a more concise format.
    """
    if value is None:
        return ''

    timesince_value = timesince(value)

    if 'day' in timesince_value:
        return timesince_value.split(',')[0] + 'd'
    elif 'hour' in timesince_value:
        return timesince_value.split(',')[0] + 'h'
    elif 'minute' in timesince_value:
        return timesince_value.split(',')[0] + 'min'
    else:
        return timesince_value
    
