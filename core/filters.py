from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg
    
@register.simple_tag
def get_model_fields(model):
    return model._meta.fields


@register.simple_tag
def querystring(request, **kwargs):
    """
    Replaces or adds query parameters to the URL.
    """
    updated = request.GET.copy()
    for key, value in kwargs.items():
        updated[key] = value
    return updated.urlencode()
