from django.conf.urls.defaults import *

# if you put the key in here it will get exposed in errors
# so probably
urlpatterns = patterns('',
    url(r'^feed/.*?/json/$', 'error.feeds.json', name="json"),
    url(r'^feed/.*?/$', 'error.feeds.atom', name="rss"),
    url(r'^group/feed/.*?/json/$', 'error.feeds.group_json', name="json"),
    url(r'^group/feed/.*?/$', 'error.feeds.group_atom', name="rss"),
    url(r'^list/$', 'error.views.errors_list', name="error-list"),
    url(r'^list/snippet/$', 'error.views.errors_snippet', name="error-snippet"),
    url(r'^groups/$', 'error.views.groups_list', name="group-list"),
    url(r'^group/(?P<pk>[\w-]+)$', 'error.views.group_edit', name="group-edit"),
    url(r'^view/(?P<pk>[\w-]+)/$', 'error.views.error_view', name="error-view"),
    url(r'^view/toggle/(?P<pk>[\w-]+)/$','error.views.error_public_toggle', name="error-toggle")
)
