from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^list/$', 'notifications.views.notifications_list', name="notification-list"),
)
