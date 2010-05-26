from app.forms import Form
from django import forms

class ErrorForm(Form):
    read = forms.ChoiceField(
                choices=(("", "All"), ("False", 'Read only'), ("True", 'Unread only')),
                widget=forms.Select, required=False
                )
    uid = forms.CharField(required=False)
            
    def as_query(self):
        # remove anything that's empty from going in the query
        data = {}
        for k, v in self.cleaned_data.items():
            if v: data[k] = v
        
        # coerce back
        if "read" in data:
            data["read"] = {"False":False, "True":True}.get(data["read"], None)
        return data
