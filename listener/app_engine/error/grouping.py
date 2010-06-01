import md5

from django.db.models import signals

from app.utils import safe_string
from error.models import Error, Group
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
    
signals.error_created.connect(default_grouping, sender=Error, dispatch_uid="default_grouping")