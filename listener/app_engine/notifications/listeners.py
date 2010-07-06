from app.utils import log
from notifications.models import Notification
from users.utils import approved_users

from error.signals import error_created

def default_notification(instance, **kw):
    """ Given an error see if we need to send a notification """
    log("Firing signal: default_notification")

    # todo, this will be changed to lookup a user profile as per
    # http://github.com/andymckay/arecibo/issues/issue/4
    if instance.priority >= 5:
        return

    notification = Notification()
    notification.error = instance
    notification.user = [ str(u.key()) for u in approved_users() ]
    notification.save()

error_created.connect(default_notification, dispatch_uid="default_notification")