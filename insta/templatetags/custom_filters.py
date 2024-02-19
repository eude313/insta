from insta.models import Like
from django import template
from django.utils.timesince import timesince
from datetime import datetime
from dateutil import parser
from django.utils import timezone

register = template.Library()

@register.filter(name='time_filter')
def shorten_time_since(value):
    """
    Shortens the time since the given value (usually a datetime) to a more concise format.
    """
    if value is None:
        return ''

    try:
        # Parse the value if it's a string
        if isinstance(value, str):
            value = parser.parse(value)

        # Check if value is a datetime object
        if not isinstance(value, datetime):
            return ''

        # Calculate the time difference
        delta = timezone.now() - value

        # Years
        if delta.days >= 365:
            years = delta.days // 365
            return f'{years}y'
        # Months
        elif delta.days >= 30:
            months = delta.days // 30
            return f'{months}m'
        # Weeks
        elif delta.days >= 7:
            weeks = delta.days // 7
            return f'{weeks}w'
        # Days
        elif delta.days > 0:
            return f'{delta.days}d'
        # Hours
        elif delta.seconds >= 3600:
            hours = delta.seconds // 3600
            return f'{hours}h'
        # Minutes
        elif delta.seconds >= 60:
            minutes = delta.seconds // 60
            return f'{minutes}min'
        # Seconds
        else:
            return f'{delta.seconds}s'
        
    except Exception as e:
        # Log the exception for debugging
        print(f"Error parsing datetime: {e}")
        return ''
    
@register.filter(name='like_filter')
def liked_icon(post, user):
    try:
        like = Like.objects.get(post=post, user=user)
        if like.is_like:
            return '<i class="bi bi-heart-fill" style="color:red;"></i>'
    except Like.DoesNotExist:
        pass

    return '<i class="bi bi-heart-fill"></i>'