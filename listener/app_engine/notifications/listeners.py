from app.utils import log
from notifications.models import Notification
from profiles.utils import get_profile
from users.utils import approved_users

from error.signals import error_created
from issues.signals import issue_created, issue_changed

def default_notification(instance, **kw):
    """ Given an error see if we need to send a notification """
    log("Firing signal: default_notification")

    users = approved_users()
    filtered = []
    for user in users:
        profile = get_profile(user)
        if profile.notification and instance.priority <= profile.notification:
            filtered.append(user)
    
    if not filtered:
        return
    
    notification = Notification()
    notification.type = "Error"
    notification.type_key = str(instance.key())
    notification.user = [ str(u.key()) for u in filtered ]
    notification.save()

error_created.connect(default_notification, dispatch_uid="default_notification")

def default_issue_notification(instance, **kw):
    """ Given an issue see default_issue_notification we need to send a notification """
    log("Firing signal: default_notification")

    users = approved_users()

    if not users.count():
        return
    
    notification = Notification()
    notification.type = "Issue"
    notification.type_key = str(instance.key())
    notification.user = [ str(u.key()) for u in users ]
    notification.save()

# turn this on when its all working
#issue_created.connect(default_issue_notification, dispatch_uid="default_issue_notification")
#issue_changed.connect(default_issue_notification, dispatch_uid="default_issue_notification")