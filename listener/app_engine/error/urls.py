from django.conf.urls.defaults import *
from error.views import LatestEntriesFeed

urlpatterns = patterns('',
    url(r'^v/1/$', 'error.views.post', name="error-post"),
    url(r'feed/$', LatestEntriesFeed(), name="rss"),
    url(r'list/', 'error.views.errors_list', name="error-list"),
    url(r'view/(?P<id>[\w-]+)/$', 'error.views.error_view', name="error-view"),    
)
