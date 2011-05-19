from error.models import Error

from error import signals

def default_public(instance, **kw):
    instance.public = True
    instance.save()

signals.error_created.connect(default_public, dispatch_uid="default_public")
