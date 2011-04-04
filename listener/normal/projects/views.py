from django.contrib.auth.decorators import user_passes_test
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404

from app.decorators import arecibo_login_required

from projects.models import Project, ProjectURL
from projects.forms import ProjectForm, ProjectURLForm


@arecibo_login_required
def project_list(request):
    projects = Project.objects.all().order_by("-name")
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
    project = get_object_or_404(Project, pk=pk)
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
    url = get_object_or_404(ProjectURL, pk=url)
    project = project = get_object_or_404(Project, pk=pk)
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