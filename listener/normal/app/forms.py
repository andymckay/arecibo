from django import forms
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


def as_blue_print(self):
    return self._html_output(u"""
    <div class="span-8 clear">
        <div %(html_class_attr)s>
            %(label)s<br />
            %(errors)s
            <span class="help">%(help_text)s</span>
            %(field)s
        </div>
    </div>
    """, u'%s', '', u'%s', False)


class Form(forms.Form):
    required_css_class = 'required'

    def as_custom(self):
        return as_blue_print(self)


class ModelForm(forms.ModelForm):
    required_css_class = 'required'

    def as_custom(self):
        return as_blue_print(self)


def as_div(self):
    if not self:
        return u''
    template = "%s"
    errors = ''.join([u'<p class="field-error">%s</p>' % conditional_escape(force_unicode(e)) for e in self])
    template = template % errors
    return mark_safe(template)


forms.util.ErrorList.__unicode__ = as_div
