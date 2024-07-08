from django import template
register = template.Library()
from num2words import num2words
from agent.models import Agent
from django.utils import timezone


@register.filter
def replace_commas(string):
    try:
        _string = round(float(string), 2)
    except:
        _string = str(string)
    _string = str(_string)
    return _string.replace(',', '.')

@register.filter
def number_in_words_ar(string):
    try:
        words = num2words(float(string), lang='ar', to="currency")
        return words
    except:
        return ""

@register.filter
def get_agent_from_id(id):
    return Agent.objects.get(id=id)


@register.filter
def getattribute(value, arg):
    return getattr(value, arg)


@register.filter
def getattr(obj, attr):
    return getattr(obj, attr)


@register.filter
def get_model_fields(model):
    return model._meta.fields

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key, "")

@register.filter
def get_prev(version, field_name):
    if version.prev_record:
        return getattr(version.prev_record, field_name)
    else:
        return None
    

@register.simple_tag
def querystring(request, **kwargs):
    """
    Replaces or adds query parameters to the URL.
    """
    updated = request.GET.copy()
    for key, value in kwargs.items():
        updated[key] = value
    return updated.urlencode()
