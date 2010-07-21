from google.appengine.ext import webapp
register = webapp.template.create_template_register()

from app.utils import trunc_string

from django.contrib.markup.templatetags.markup import markdown as real_markdown

@register.filter
def trunc(value, arg):
    "Removes all values of arg from the given string"
    return trunc_string(value, arg)

@register.filter
def markdown(value, arg=""):
    return real_markdown(value, arg)
