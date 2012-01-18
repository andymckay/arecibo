from django.contrib.syndication.views import Feed
from django.core import serializers
from django.http import HttpResponse

from app.utils import has_private_key
from error.views import get_filtered, get_group_filtered

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

@has_private_key
def json(request):
    form, queryset = get_filtered(request)
    response = HttpResponse(mimetype="text/javascript")
    json_serializer = serializers.get_serializer("json")()
    json_serializer.serialize(queryset[:20], ensure_ascii=False, stream=response)
    return response

class group(Feed):
    title = "Arecibo Errors by Groups"
    link = "/groups/"
    description = "Arecibo Errors by Groups"
    subtitle = "Arecibo Errors by Groups"

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
def group_atom(request):
    feedgen = base()
    feedgen.request = request
    return feedgen(request)

@has_private_key
def group_json(request):
    form, queryset = get_group_filtered(request)
    response = HttpResponse(mimetype="text/javascript")
    json_serializer = serializers.get_serializer("json")()
    json_serializer.serialize(queryset[:20], ensure_ascii=False, stream=response)
    return response
