from datetime import datetime

from error.signals import error_created
from error.models import Error
from notifications.models import Notification
from users.utils import approved_users

def default_notification(instance, **kw):
    """ Given an error see if we need to send a notification """
    # todo, this will be changed to lookup a user profile as per
    # http://github.com/andymckay/arecibo/issues/issue/4
    if instance.priority > 5:
        return
    
    notification = Notification()
    notification.error = instance
    notification.user = [ str(u.__key__) for u in approved_users() ]
    notification.save()
    
error_created.connect(default_notification, sender=Error, dispatch_uid="default_notification")