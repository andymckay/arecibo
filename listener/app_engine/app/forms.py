from django import forms

def as_blue_print(self):
    return self._html_output(u"""
    <div class="span-8">
        %(errors)s
        %(label)s<br />
        %(field)s
        <span class="help">%(help_text)s</span>
    </div>
    """, u'%s', '', u'%s', False)

class Form(forms.Form):
    def as_custom(self):
        return as_blue_print(self)

class ModelForm(forms.ModelForm):
    def as_custom(self):
        return as_blue_print(self)

from django.utils.html import conditional_escape
from django.utils.encoding import smart_unicode, StrAndUnicode, force_unicode
from django.utils.safestring import mark_safe

def as_div(self):
    if not self: return u''
    template = "%s"
    errors = ''.join([u'<p class="error">%s</p>' % conditional_escape(force_unicode(e)) for e in self])
    template = template % errors
    return mark_safe(template)

forms.util.ErrorList.__unicode__ = as_div