from django import forms
from django.utils.translation import ugettext as _

from app.forms import ModelForm

from appengine_django.auth.models import User

class UserForm(ModelForm):
    is_staff = forms.BooleanField(required=False, label=_("Access to Arecibo"))
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "is_staff")