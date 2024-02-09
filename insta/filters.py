from django import template
from .models import Like

register = template.Library()

@register.filter
def liked_icon(post, user):
    try:
        like = Like.objects.get(post=post, user=user)
        if like.is_like:
            return '<i class="bi bi-heart-fill" style="color:red;"></i>'
    except Like.DoesNotExist:
        pass

    return '<i class="bi bi-heart-fill"></i>'
