from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader

from error.models import Error, Group
from error.forms import ErrorForm, GroupForm
from error.signals import error_created

from app.decorators import arecibo_login_required
from app.utils import render_plain, render_json, not_allowed
from app.paginator import Paginator, get_page


def get_group_filtered(request):
    form = GroupForm(request.GET or None)
    if form.is_valid():
        queryset = form.as_query()
    else:
        queryset = Group.objects.all()
        queryset.order_by("-timestamp")

    return form, queryset


def get_filtered(request):
    form = ErrorForm(request.GET or None)
    if form.is_valid():
        queryset = form.as_query()
    else:
        queryset = Error.objects.all()
        queryset.order_by("-timestamp")

    return form, queryset


@arecibo_login_required
def errors_list(request):
    form, queryset = get_filtered(request)
    paginated = Paginator(queryset, 50)
    page = get_page(request, paginated)
    if request.GET.get("lucky") and len(page.object_list):
        return HttpResponseRedirect(reverse("error-view", args=[page.object_list[0].id,]))
    return direct_to_template(request, "list.html", extra_context={
        "page": page,
        "nav": {"selected": "list", "subnav": "list"},
        "form": form,
        "refresh": True
        })


@arecibo_login_required
@render_json
def errors_snippet(request, pk=None):
    form, queryset = get_filtered(request)
    paginated = Paginator(queryset, 50)
    page = get_page(request, paginated)
    template = loader.get_template('list-snippet.html')
    html = template.render(RequestContext(request, {"object_list": page.object_list, }))
    return {"html":html, "count": len(page.object_list) }


@arecibo_login_required
def groups_list(request):
    form, queryset = get_group_filtered(request)
    paginated = Paginator(queryset, 50)
    page = get_page(request, paginated)
    return direct_to_template(request, "group.html", extra_context={
        "page": page,
        "form": form,
        "nav": {"selected": "list", "subnav": "group"},
        })


@arecibo_login_required
def error_public_toggle(request, pk):
#    error = Error.objects.get(pk=pk)
#    if request.method.lower() == "post":
#        if error.public:
#            error.public = False
#        else:
#            error.public = True
#        error.save()
    return HttpResponseRedirect(reverse("error-view", args=[error.id,]))


@arecibo_login_required
def error_view(request, pk):
    error = Error.objects.get(pk=pk)

    if not error.read:
        error.read = True
        error.save()

    return direct_to_template(request, "view.html", extra_context={
        "error":error,
        "nav": {"selected": "list"},
        })
