from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^users/$', 'users.views.user_list', name="user-list"),
    url(r'^users/edit/(?P<pk>[\w-]+)/$', 'users.views.user_edit', name="user-edit"),
    url(r'^users/create/$', 'users.views.user_create', name="user-create"),
    url(r'^users/password/$', 'users.views.user_password', name="user-password"),
    
    url(r'^login/$', 'users.views.login', name="login"),
    url(r'^logout/$', 'users.views.logout', name="logout"),
)
