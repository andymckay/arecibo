from django.contrib.syndication.views import Feed

from app.utils import has_private_key
from error.views import get_filtered

class base(Feed):
    title = "Arecibo Errors"
    link = "/list/"
    description = "Arecibo Errors"
    subtitle = "Arecibo Errors"
    
    def __init__(self, *args, **kw):
        Feed.__init__(self, *args, **kw)
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