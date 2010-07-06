from django import forms
from app.forms import ModelForm

from projects.models import Project, ProjectURL, stage_choices

class ProjectForm(ModelForm):
    name = forms.CharField(required=True, label="Name")
    description = forms.CharField(required=False, label="Description", widget=forms.Textarea)

    class Meta:
        model = Project

class ProjectURLForm(ModelForm):
    url = forms.CharField(required=True, label="Domain")
    stage = forms.CharField(
        required=True, label="Project stage",
        widget=forms.Select(choices=stage_choices)
        )

    class Meta:
        model = ProjectURL
        fields = ("url", "stage")