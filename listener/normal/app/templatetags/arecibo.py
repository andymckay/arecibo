from app.utils import trunc_string
from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@register.filter
@stringfilter
def trunc(value, arg):
    "Removes all values of arg from the given string"
    return trunc_string(value, arg)
