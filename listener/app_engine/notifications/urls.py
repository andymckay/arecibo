from django.conf.urls.defaults import *
from error.views import LatestEntriesFeed

urlpatterns = patterns('',
    url(r'^list/$', 'notifications.views.notification_list', name="notification-list"),
)
