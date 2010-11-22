from django import forms
from django.utils.translation import ugettext as _
from django.core.validators import EMPTY_VALUES

from app.forms import ModelForm, Form
from app.fields import OurModelChoiceField, OurModelChoiceIterator
from issues.models import Issue, Comment, IssueProjectURL
from appengine_django.auth.models import User
from error.forms import Filter

priorities = ([1,_("High")], [3, _("Medium")], [5, _("Low")])
states = (
    ["open", _("Open")],
    ["accepted", _("Accepted")],
    ["work_progress", _("Work in progress")],
    ["testing", _("Testing")],
    ["approved", _("Approved")],
    ["deploy_progress", _("Deploy in process")],
    ["deployed", _("Deployed")],
    ["rejected", _("Rejected")],
    )
states_first_empty = list(states)
states_first_empty.insert(0, ["", "-------"])

issue_project_url_statuses = (
    ["fixed", _("Fixed")],
    ["not_fixed", _("Not Fixed")],
    ["not_relevant", _("Not relevant")],
)

class IssueProjectURLForm(ModelForm):
    status = forms.ChoiceField(choices=issue_project_url_statuses,
        widget=forms.Select, required=False)

    class Meta:
        model = IssueProjectURL
        fields = ("status")

class IssueListForm(Filter):
    status = forms.ChoiceField(choices=states_first_empty, widget=forms.Select, required=False)
    assigned = OurModelChoiceField(required=False,
        queryset=User.all().filter("is_staff = ", True),
        model=User)

    def as_query(self):
        return super(IssueListForm, self).as_query("Issue")

class IssueForm(ModelForm):
    title = forms.CharField(required=False, label=_("Title"),
        widget=forms.TextInput(attrs={"size":100}))
    raw = forms.CharField(required=False, label=_("URL"),
        widget=forms.TextInput(attrs={"size":100}))
    description = forms.CharField(required=True,
        help_text=_("A description, markdown syntax possible."),
        widget=forms.Textarea(attrs={"cols": 100, "rows": 10}))
    priority = forms.IntegerField(required=False,
        widget=forms.Select(choices=priorities))
    status = forms.CharField(required=False,
        widget=forms.Select(choices=states))
    assigned = OurModelChoiceField(required=False,
        queryset=User.all().filter("is_staff = ", True),
        model=User)
    
    class Meta:
        model = Issue
        fields = ("raw", "description", "title", "priority", "assigned",
                    "project", "status")

class GroupForm(Form):
    group = forms.CharField(required=False, widget=forms.HiddenInput())

class UpdateForm(Form):
    status = forms.CharField(required=False, widget=forms.Select(choices=states))
    assigned = OurModelChoiceField(required=False,
        queryset=User.all().filter("is_staff = ", True),
        model=User)
    text = forms.CharField(required=False, label=_("Comments"),
        widget = forms.Textarea(
            attrs={"cols": 100, "rows": 10}
            ),
        help_text=_("A description, markdown syntax possible.")
        )
