try:
    from hashlib import md5
except ImportError:
    from md5 import md5 

from django.db.models import F

from app.utils import safe_string, log
from error.models import Group, Error

from error.agent import get
from error import signals

def generate_key(instance):
    keys = ["type", "server", "msg", "status", "domain"]
    hsh = None

    for key in keys:
        value = safe_string(getattr(instance, key))
        if value:
            if not hsh:
                hsh = md5()
            hsh.update(value.encode("ascii", "ignore"))

    return hsh

def default_grouping(instance, **kw):
    """ Given an error, see if we can fingerprint it and find similar ones """
    log("Firing signal: default_grouping")

    hsh = generate_key(instance)
    if hsh:
        digest = hsh.hexdigest()
        try:
            created = False
            group = Group.objects.get(uid=digest)
            group.count = F('count')+getattr(instance, 'count', 1)
            group.save()
        except Group.DoesNotExist:
            created = True
            group = Group.objects.create(uid=digest, count=getattr(instance, 'count', 1))

        instance.group = group
        instance.save()

        if created:
            signals.group_assigned.send(sender=group.__class__, instance=group)
        signals.error_assigned.send(sender=instance.__class__, instance=instance)

signals.error_created.connect(default_grouping,
                              dispatch_uid="default_grouping")

def default_browser_parsing(instance, **kw):
    log("Firing signal: default_browser_parsing")
    if instance.user_agent:
        bc = get()
        if bc:
            b = bc(instance.user_agent)
            if b:
                instance.user_agent_short = b.name()
                instance.operating_system = b.platform()

    instance.user_agent_parsed = True
    instance.save()

signals.error_created.connect(default_browser_parsing,
                              dispatch_uid="default_browser_parsing")
