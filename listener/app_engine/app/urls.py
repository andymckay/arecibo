from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'app.views.index', name="index"),
    url(r'^accounts/login/$', 'app.views.login', name="login"), 
    url(r'^accounts/logout/$', 'app.views.logout', name="logout"), 
)
