from django.conf.urls.defaults import *

# if you put the key in here it will get exposed in errors
# so probably
urlpatterns = patterns('',
    url(r'^$', 'stats.views.view', name="stats-view"),
    url(r'^generate/$', 'stats.views.start', name="stats-start"),
    url(r'^generate/action/(?P<action>[\w-]+)/(?P<pk>[\w-]+)/$', 'stats.views.get_action', name="stats-action"),

)
