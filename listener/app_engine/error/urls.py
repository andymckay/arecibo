from django.conf.urls.defaults import *

# if you put the key in here it will get exposed in errors
# so probably
urlpatterns = patterns('',
    url(r'^feed/.*?/$', 'error.feeds.atom', name="rss"),
    url(r'^list/$', 'error.views.errors_list', name="error-list"),
    url(r'^list/snippet/$', 'error.views.errors_snippet', name="error-snippet"),
    url(r'^groups/$', 'error.views.groups_list', name="group-list"),
    url(r'^view/(?P<pk>[\w-]+)/$', 'error.views.error_view', name="error-view"),
    url(r'^send/created/(?P<pk>[\w-]+)/$', 'error.views.send_signal', name="error-created"),
)
