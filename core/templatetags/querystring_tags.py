from django import template

register = template.Library()

@register.simple_tag
def querystring(request, **kwargs):
    """
    Replaces or adds query parameters to the URL.
    """
    updated = request.GET.copy()
    for key, value in kwargs.items():
        updated[key] = value
    return updated.urlencode()