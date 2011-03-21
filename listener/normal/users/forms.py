from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       SetPasswordForm)
from django.utils.translation import ugettext as _

from app.forms import Form, ModelForm


class LoginForm(Form, AuthenticationForm):
    pass


class CreateForm(ModelForm, UserCreationForm):
    username = forms.RegexField(max_length=30, regex=r'^[\w.@+-]+$',
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1",
                  "password2", "email")
        
        
class EditForm(ModelForm):
    username = forms.CharField(max_length=30)
    is_staff = forms.BooleanField(required=False, label=_("Access to Arecibo"))
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "is_staff")
        

class PasswordForm(Form, SetPasswordForm):
    pass