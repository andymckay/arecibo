from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'app.views.index', name="index"),
    url(r'^lib/error.js', 'app.views.javascript_client', name="error-javascript"),
    url(r'^lib/error-compress.js', 'app.views.javascript_client', name="error-javascript-compressed"),
    url(r'^setup$', 'app.views.setup', name="setup")
)
