import md5

from django.utils.translation import ugettext as _

from app.utils import safe_string, log
from issues import signals
from issues.models import IssueProjectURL

def default_add_issue(instance, **kw):
    log("Firing signal: default_add_issue")
    instance.add_log(_("Issue created."))

signals.issue_created.connect(default_add_issue, dispatch_uid="default_add_issue")

def default_add_comment(instance, **kw):
    log("Firing signal: default_add_comment")
    instance.issue.add_log(_("Comment created."))

signals.comment_created.connect(default_add_comment, dispatch_uid="default_add_comment")

def default_add_project_urls(instance, **kw):
    log("Firing signal: default_add_project_urls")
    if instance.project:
        for project_url in instance.project.projecturl_set:
            issue_project_url = IssueProjectURL(
                issue=instance,
                project_url=project_url,
                status="not_fixed")
            issue_project_url.save()

signals.issue_created.connect(default_add_project_urls, dispatch_uid="default_add_project_urls")
