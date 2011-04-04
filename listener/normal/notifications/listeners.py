from app.utils import log
from notifications.models import Notification
from users.utils import approved_users

from error.signals import error_created

def default_notification(instance, **kw):
    """ Given an error see if we need to send a notification """
    log("Firing signal: default_notification")

    if instance.priority >= 5:
        return

    users = approved_users()
    if not users.count():
        return
    
    notification = Notification()
    notification.notifier = instance
    notification.save()
    for user in users:
        notification.user.add(user)
    

error_created.connect(default_notification, dispatch_uid="default_notification")