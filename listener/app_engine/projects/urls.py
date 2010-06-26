from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'projects.views.project_list', name="projects-list"),

    url(r'^add/url/(?P<pk>[\w-]+)/$', 'projects.views.project_url_add', name="projects-url-add"),
    url(r'^edit/url/(?P<pk>[\w-]+)/(?P<url>[\w-]+)/$', 'projects.views.project_url_edit', name="projects-url-edit"),

    url(r'^add/$', 'projects.views.project_add', name="projects-add"),
    url(r'^edit/(?P<pk>[\w-]+)/$', 'projects.views.project_edit', name="projects-edit"),

)
