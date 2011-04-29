from app.utils import trunc_string
from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@register.filter
@stringfilter
def trunc(value, arg):
    return trunc_string(value, arg)
