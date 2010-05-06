from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^v/1/$', 'error.views.post'),
)
