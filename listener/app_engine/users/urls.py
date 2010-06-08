from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^users/$', 'users.views.user_list', name="user-list"),
    url(r'^users/change/(?P<pk>[\w-]+)/$', 'users.views.user_change', name="user-change"),
)
