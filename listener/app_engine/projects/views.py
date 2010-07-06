from django.contrib.auth.decorators import user_passes_test
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader

from google.appengine.ext import db

from projects.models import Project, ProjectURL
from projects.forms import ProjectForm, ProjectURLForm

@user_passes_test(lambda u: u.is_staff)
def project_list(request):
    projects = Project.all().order("-name")
    return direct_to_template(request, "project_list.html", extra_context={
        "page": projects,
        "nav": {"selected": "projects", "subnav": "list"},
    })

@user_passes_test(lambda u: u.is_staff)
def project_add(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("projects-list"))
    return direct_to_template(request, "project_add.html", extra_context={
        "form": form,
        "nav": {"selected": "projects",},
    })

@user_passes_test(lambda u: u.is_staff)
def project_edit(request, pk):
    form = ProjectForm(request.POST or None, instance=Project.get(pk))
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("projects-list"))
    return direct_to_template(request, "project_edit.html", extra_context={
        "form": form,
        "nav": {"selected": "projects",},
    })

@user_passes_test(lambda u: u.is_staff)
def project_url_add(request, pk):
    project = Project.get(pk)
    form = ProjectURLForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.project = project
        obj.save()
        return HttpResponseRedirect(reverse("projects-list"))
    return direct_to_template(request, "project_url_add.html", extra_context={
        "form": form,
        "project": project,
        "nav": {"selected": "projects",},
    })

@user_passes_test(lambda u: u.is_staff)
def project_url_edit(request, pk, url):
    url = ProjectURL.get(url)
    project = Project.get(pk)
    form = ProjectURLForm(request.POST or None, instance=url)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.project = project
        obj.save()
        return HttpResponseRedirect(reverse("projects-list"))
    return direct_to_template(request, "project_url_edit.html", extra_context={
        "form": form,
        "project": project,
        "nav": {"selected": "projects",},
    })
