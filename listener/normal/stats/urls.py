from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'stats.views.stats_view', name="stats-view"),
    url(r'^view/(?P<key>[\w-]+)/$', 'stats.views.stats_view', name="stats-view"),
)
