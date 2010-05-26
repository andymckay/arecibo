from django import forms

def as_blue_print(self):
    return self._html_output(u"""
    <div class="span-12 prepend-1 append-bottom">
        %(errors)s
        <div class="span-3" style="text-align: right">%(label)s</div>
        <div class="span-9 last">%(field)s</div>
        <span class="span-9 help clear">%(help_text)s</span>
    </div>
    """, u'%s', '', u'%s', False)

class Form(forms.Form):
    def as_custom(self):
        return as_blue_print(self)

class ModelForm(forms.ModelForm):
    def as_custom(self):
        return as_blue_print(self)