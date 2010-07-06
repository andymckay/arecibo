from app.utils import log

from projects.models import Project
from error import signals 

def lookup_domain(domain):
    # given a domain, find the project
    projects = Project.all()
    for project in projects:
        for url in project.projecturl_set:
            if domain == url.url:
                return url
     
def default_project(instance, **kw):
    log("Firing signal: default_project")
    if instance.project_url:
        return
        
    error = instance.sample()
    if error:
        domain = lookup_domain(error.domain)
        if domain:
            instance.project_url = domain
            instance.save()
    
signals.group_assigned.connect(default_project, dispatch_uid="default_browser_parsing")      