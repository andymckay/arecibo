from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^v/1/$', 'receiving.http.post', name="error-post"),
    url(r'^_ah/mail/django-.*', 'receiving.mail_django.post', name="mail-django-post"),
    url(r'^_ah/mail/.*', 'receiving.mail.post', name="mail-post"),
)
