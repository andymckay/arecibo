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