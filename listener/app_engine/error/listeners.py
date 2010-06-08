import md5

from app.utils import safe_string, log
from error.models import Error, Group
from error.agent import get
from error import signals

def generate_key(instance):
    keys = ["type", "server", "msg", "status",]
    hsh = None

    for key in keys:  
        value = safe_string(getattr(instance, key))
        if value:
            if not hsh:
                hsh = md5.new()
            hsh.update(value.encode("ascii", "ignore"))
    
    return hsh
    
def default_grouping(instance, **kw):
    """ Given an error, see if we can fingerprint it and find similar ones """
    # prevent an infinite loop
    log("Firing signal: default_grouping")
    if instance.group:
        return
        
    hsh = generate_key(instance)
    if hsh:
        digest = hsh.hexdigest()
        try:
            group = Group.all().filter("uid = ", digest)[0]
            group.save()
        except IndexError:
            group = Group()
            group.uid = digest
            group.save()

        instance.group = group
        instance.save()

signals.error_created.connect(default_grouping, dispatch_uid="default_grouping")


def default_browser_parsing(instance, **kw):
    # prevent an infinite loop
    log("Firing signal: default_browser_parsing")
    if instance.user_agent_parsed:
        return

    if instance.user_agent:
        bc = get()
        b = bc(instance.user_agent)
        if b:
            instance.user_agent_short = b.name()
            instance.operating_system = b.platform()
    
    instance.user_agent_parsed = True
    instance.save()

signals.error_created.connect(default_browser_parsing, dispatch_uid="default_browser_parsing")