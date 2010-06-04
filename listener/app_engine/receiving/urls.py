from django.conf.urls.defaults import *
from error.views import LatestEntriesFeed

urlpatterns = patterns('',
    url(r'^v/1/$', 'receiving.http.post', name="error-post"),
    url(r'^_ah/mail/.*', 'receiving.mail.post', name="mail-post"),
)
