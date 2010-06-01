from django.contrib.auth.decorators import user_passes_test
from django.views.generic.simple import direct_to_template

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.http import HttpResponse

from google.appengine.ext import db

from error.models import Error, Group
from error.forms import ErrorForm
from error.signals import error_created

from app.paginator import Paginator, get_page

# these aren't used directly
from notifications import listeners
from error import listeners
try:
    from custom import listeners
except ImportError:
    pass
    
class LatestEntriesFeed(Feed):
    title = "Arecibo Errors"
    link = "/list/"
    description = "Arecibo Errors"
    feed_type = Atom1Feed
    subtitle = "Arecibo Errors"
    
    def items(self):
        return Error.all().order("-timestamp")[:20]

    def item_title(self, item): return item.title
    def item_description(self, item): return item.description
    def item_pubdate(self, item): return item.timestamp

def send_signal(request, pk):
    error = Error.get(pk)        
    if not error.create_signal_sent:
        error.create_signal_sent = True
        error.save()
        error_created.send(sender=error.__class__, instance=error)
        return HttpResponse("Signal sent")
    return HttpResponse("Signal not sent")

def get_filtered(request):
    form = ErrorForm(request.GET or None)
    queryset = db.Query(Error)
    if form.is_valid():
        for key, value in form.as_query().items():
            queryset.filter("%s = " % key, value)
            
    queryset.order("-timestamp")
    return form, queryset

@user_passes_test(lambda u: u.is_staff)
def errors_list(request):
    form, queryset = get_filtered(request)
    paginated = Paginator(queryset, 50)
    page = get_page(request, paginated)
    return direct_to_template(request, "list.html", extra_context={
        "page": page, 
        "nav": {"selected": "list", "subnav": "list"},
        "form": form
        })
        
@user_passes_test(lambda u: u.is_staff)
def groups_list(request):
    queryset = Group.all().order("-timestamp")
    paginated = Paginator(queryset, 50)
    page = get_page(request, paginated)
    return direct_to_template(request, "group.html", extra_context={
        "page": page, 
        "nav": {"selected": "list", "subnav": "group"},
        })


@user_passes_test(lambda u: u.is_staff)
def error_view(request, pk):
    error = Error.get(pk)
    if not error.read:
        error.read = True
        error.save()
    return direct_to_template(request, "view.html", extra_context={"error":error})
