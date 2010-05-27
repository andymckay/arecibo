from django.db.models import signals

from error.models import Error, Group

def find_or_create_grouping(self, instance, **kw):
    

signals.post_save(find_or_create_grouping, sender=Error, dispatch_uid="find_or_create_grouping")