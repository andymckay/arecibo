from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^users/$', 'users.views.user_list', name="user-list"),
    url(r'^users/edit/(?P<pk>[\w-]+)/$', 'users.views.user_edit', name="user-edit"),
)
