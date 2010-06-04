from django.conf.urls.defaults import *
from error.views import LatestEntriesFeed

urlpatterns = patterns('',
    url(r'^list/$', 'notifications.views.notifications_list', name="notification-list"),
    url(r'^send/$', 'notifications.views.notifications_send', name="notification-send"),
    url(r'^cleanup/$', 'notifications.views.notifications_cleanup', name="notification-clean"),
)
