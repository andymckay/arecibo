from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'issues.views.issue_list', name="issues-list"),
    url(r'^add/$', 'issues.views.issue_add', name="issues-add"),

    url(r'^edit/project-url/(?P<pk>[\w-]+)/$', 'issues.views.edit_project_url', name="issues-project-url"),
    url(r'^edit/(?P<pk>[\w-]+)/$', 'issues.views.issue_edit', name="issues-edit"),

    url(r'^view/(?P<pk>[\w-]+)/$', 'issues.views.issue_view', name="issues-view"),
    url(r'^view/logs/(?P<pk>[\w-]+)/$', 'issues.views.issue_log_view', name="issues-log-view"),

    url(r'^add/comment/(?P<pk>[\w-]+)/$', 'issues.views.comment_add', name="issues-add-comment"),
)
