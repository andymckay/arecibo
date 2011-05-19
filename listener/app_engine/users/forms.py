from django import forms
from django.utils.translation import ugettext as _

from app.forms import ModelForm

from appengine_django.auth.models import User
from profiles.models import Profile

class UserForm(ModelForm):
    is_staff = forms.BooleanField(required=False, label=_("Access to Arecibo"))
        
    class Meta:
        model = User
        fields = ("is_staff", "first_name", "last_name", "email")
        
choices = [ [x,x] for x in range(0, 10) ]
choices[0][1] = "No notifications"

class ProfileForm(ModelForm):
    notification = forms.IntegerField(
                         required=False,
                         label=_("Send notification at this priority level and above"),
                         widget=forms.Select(choices=choices))
    
    class Meta:
        model = Profile
        fields = ("notification",)