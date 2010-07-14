from django.contrib.auth.decorators import user_passes_test
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader

from google.appengine.ext import db

from error.models import Error, Group
from error.forms import ErrorForm, GroupForm
from error.signals import error_created

from app.utils import render_plain, render_json
from app.paginator import Paginator, get_page

# these aren't used directly, but if we don't import them here they
# won't get imported
from notifications import listeners as notifications_listeners
from projects import listeners as projects_listeners
from error import listeners as error_listeners
from issues import listeners as error_listeners

try:
    from custom import listeners as custom_listeners
except ImportError:
    pass

def send_signal(request, pk):
    error = Error.get(pk)
    if not error.create_signal_sent:
        error.create_signal_sent = True
        error.save()
        error_created.send(sender=error.__class__, instance=error)
        return render_plain("Signal sent")
    return render_plain("Signal not sent")

def get_group_filtered(request):
    form = GroupForm(request.GET or None)
    if form.is_valid():
        queryset = form.as_query()
    else:
        queryset = db.Query(Group)
        queryset.order("-timestamp")

    return form, queryset

def get_filtered(request):
    form = ErrorForm(request.GET or None)
    if form.is_valid():
        queryset = form.as_query()
    else:
        queryset = db.Query(Error)
        queryset.order("-timestamp")

    return form, queryset

@user_passes_test(lambda u: u.is_staff)
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

@user_passes_test(lambda u: u.is_staff)
@render_json
def errors_snippet(request, pk=None):
    form, queryset = get_filtered(request)
    paginated = Paginator(queryset, 50)
    page = get_page(request, paginated)
    template = loader.get_template('list-snippet.html')
    html = template.render(RequestContext(request, {"object_list": page.object_list, }))
    return {"html":html, "count": len(page.object_list) }

@user_passes_test(lambda u: u.is_staff)
def groups_list(request):
    form, queryset = get_group_filtered(request)
    paginated = Paginator(queryset, 10)
    page = get_page(request, paginated)
    return direct_to_template(request, "group.html", extra_context={
        "page": page,
        "form": form,
        "nav": {"selected": "list", "subnav": "group"},
        })

@user_passes_test(lambda u: u.is_staff)
def error_view(request, pk):
    error = Error.get(pk)
    if not error.read:
        error.read = True
        error.save()
    return direct_to_template(request, "view.html", extra_context={
        "error":error,
        "nav": {"selected": "list"},
        })
