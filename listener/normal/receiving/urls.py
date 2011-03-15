from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^v/1/$', 'receiving.http.post', name="error-post"),
)
