from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'app.views.index', name="index"),
    url(r'^lib/error.js', 'app.views.javascript_client', name="error-javascript"),
    url(r'^lib/error-compress.js', 'app.views.javascript_client', name="error-javascript-compressed"),
    url(r'^accounts/login/$', 'app.views.login', name="login"), 
    url(r'^accounts/logout/$', 'app.views.logout', name="logout"), 
    url(r'^setup$', 'app.views.setup', name="setup")
)
