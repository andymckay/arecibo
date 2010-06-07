from django.contrib.auth.decorators import user_passes_test
from django.views.generic.simple import direct_to_template

from django.contrib.syndication.views import Feed
from django.http import HttpResponse

from google.appengine.ext import db

from app.utils import has_private_key
from error.models import Error
from error.views import get_filtered
    
class base(Feed):
    title = "Arecibo Errors"
    link = "/list/"
    description = "Arecibo Errors"
    subtitle = "Arecibo Errors"
    
    def __init__(self, *args, **kw):
        res = Feed.__init__(self, *args, **kw)
        self.request = None
        
    def items(self):
        form, queryset = get_filtered(self.request)
        return queryset[:20]

    def item_title(self, item): return item.title
    def item_description(self, item): return item.description
    def item_pubdate(self, item): return item.timestamp

@has_private_key
def atom(request):
    feedgen = base()
    feedgen.request = request
    return feedgen(request)