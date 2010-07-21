from django.contrib.auth.decorators import user_passes_test
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.forms.formsets import formset_factory

from google.appengine.ext import db
from app.paginator import Paginator, get_page
from app.utils import safe_int

from error.models import Group

from issues.models import Issue, Comment, Log, IssueProjectURL, IssueGroup
from issues.forms import IssueForm, UpdateForm, IssueListForm, IssueProjectURLForm, GroupForm
from issues.forms import issue_project_url_statuses

from userstorage.utils import get_user

def get_issues_filtered(request):
    form = IssueListForm(request.GET or None)
    if form.is_valid():
        queryset = form.as_query()
    else:
        queryset = db.Query(Issue)
        queryset.order("-timestamp")

    return form, queryset

def issue_by_number(pk):
    """ Get's the issue by a primary key or a number, i like hacking the url so
        you can just put in a number in the URL """
    number = safe_int(pk)
    if number:
        issues = Issue.all().filter("number = ", number)
        return issues[0]
    else:
        return Issue.get(pk)

@user_passes_test(lambda u: u.is_staff)
def issue_list(request):
    form, queryset = get_issues_filtered(request)
    paginated = Paginator(queryset, 50)
    page = get_page(request, paginated)
    return direct_to_template(request, "issue_list.html", extra_context={
        "page": page,
        "form": form,
        "nav": {"selected": "issues", "subnav": "list"},
    })

@user_passes_test(lambda u: u.is_staff)
def issue_log_view(request, pk):
    issue = issue_by_number(pk)
    logs = Log.all().filter("issue = ", issue)
    paginated = Paginator(logs, 50)
    page = get_page(request, paginated)
    return direct_to_template(request, "issue_log_list.html", extra_context={
        "page": page,
        "issue": issue,
        "nav": {"selected": "issues", "subnav": "list"},
    })

@user_passes_test(lambda u: u.is_staff)
def issue_view(request, pk):
    issue = issue_by_number(pk)
    return direct_to_template(request, "issue_view.html", extra_context={
        "issue": issue,
        "get_user": get_user(),
        "nav": {"selected": "issues"}
    })

@user_passes_test(lambda u: u.is_staff)
def issue_add(request):
    issue_form = IssueForm(request.POST or request.GET or None)
    group_form = GroupForm(request.POST or request.GET or None)
    if issue_form.is_valid() and group_form.is_valid():
        obj = issue_form.save(commit=False)
        obj.creator = request.user
        obj.save()

        if group_form.cleaned_data.get("group"):
            group = Group.get(group_form.cleaned_data["group"])
            IssueGroup(group=group, issue=obj).save()

        return HttpResponseRedirect(reverse("issues-list"))
    return direct_to_template(request, "issue_add.html", extra_context={
        "issue_form": issue_form,
        "group_form": group_form,
        "nav": {"selected": "issues", "subnav": "add"},
    })

@user_passes_test(lambda u: u.is_staff)
def issue_edit(request, pk):
    issue = issue_by_number(pk)
    form = IssueForm(request.POST or None, instance=issue)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect(reverse("issues-view", args=[pk,]))
    return direct_to_template(request, "issue_edit.html", extra_context={
        "form": form,
        "issue": issue,
        "nav": {"selected": "issues",},
    })

@user_passes_test(lambda u: u.is_staff)
def edit_project_url(request, pk):
    issue = Issue.get(pk)
    urls = IssueProjectURL.all().filter("issue = ", issue)
    url_ids = dict([ (url.id, url) for url in urls ])
    if request.POST:
        for key, value in request.POST.items():
            if key in url_ids:
                assert value in [ i[0] for i in issue_project_url_statuses ], \
                    "%s not in %s" % (value, issue_project_url_statuses)
                url_ids[key].status = value
                url_ids[key].save()
        return HttpResponseRedirect(reverse("issues-view", args=[pk,]))
    return direct_to_template(request, "issue_project_url.html", extra_context={
        "issue": issue,
        "urls": urls,
        "issue_project_url_statuses": issue_project_url_statuses,
        "nav": {"selected": "issues",},
    })

@user_passes_test(lambda u: u.is_staff)
def comment_add(request, pk):
    issue = issue_by_number(pk)
    initial={"status":issue.status,}
    if issue.assigned:
        initial["assigned"] = issue.assigned.pk
    form = UpdateForm(request.POST or None, initial=initial)
    if form.is_valid():
        if "text" in form.cleaned_data:
            comment = Comment()
            comment.text = form.cleaned_data["text"]
            comment.issue = issue
            comment.creator = request.user
            comment.save()

        if "status" in form.cleaned_data and issue.status != form.cleaned_data["status"]:
            issue.add_log("Status changed from %s to %s" % (issue.status, form.cleaned_data["status"]))
            issue.status = form.cleaned_data["status"]
            issue.save()

        if "assigned" in form.cleaned_data and issue.assigned != form.cleaned_data["assigned"]:
            issue.add_log("Reassigned from %s to %s" % (issue.assigned, form.cleaned_data["assigned"]))
            issue.assigned = form.cleaned_data["assigned"]
            issue.save()

        return HttpResponseRedirect(reverse("issues-view", args=[pk,]))
    return direct_to_template(request, "comment_add.html", extra_context={
        "form": form,
        "issue": issue,
        "nav": {"selected": "issues"},
    })
