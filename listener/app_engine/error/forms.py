from app.forms import Form
from django import forms

from error.models import Error, Group

read_choices = (("", "All"), ("False", 'Read only'), ("True", 'Unread only'))
priority_choices = [ (r, r) for r in range(1, 11)]
priority_choices.insert(0, ("", "All"))

status_choices = ['100', '101', '102', '200', '201', '202', '203', 
'204', '205', '206', '207', '226', '300', '301', '302', '303', '304', 
'305', '307', '400', '401', '402', '403', '404', '405', '406', '407', 
'408', '409', '410', '411', '412', '413', '414', '415', '416', '417',
'422', '423', '424', '426', '500', '501', '502', '503', '504', '505', 
'507', '510']
status_choices = [ (r, r) for r in status_choices ]
status_choices.insert(0, ("", "All"))

def safe_int(key):
    try:
        return int(key)
    except (ValueError, AttributeError):
        return None

class ErrorForm(Form):
    priority = forms.ChoiceField(choices=priority_choices, widget=forms.Select, required=False)
    status = forms.ChoiceField(choices=status_choices, widget=forms.Select, required=False)
    read = forms.ChoiceField(choices=read_choices, widget=forms.Select, required=False)
    domain = forms.CharField(required=False)
    uid = forms.CharField(required=False)
    group = forms.CharField(required=False) 
    
    def as_query(self):
        # remove anything that's empty from going in the query
        data = {}
        for k, v in self.cleaned_data.items():
            if v: data[k] = v
        # coerce
        if "read" in data:
            data["read"] = {"False":False, "True":True}.get(data["read"], None)
        if "priority" in data:
            data["priority"] = safe_int(data["priority"])
        if "group" in data:
            data["group"] = Group.all().filter("uid = ", data["group"])[0].key()
        return data
