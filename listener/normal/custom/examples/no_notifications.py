from notifications.listeners import default_notification
from error.signals import error_created

error_created.disconnect(default_notification, dispatch_uid="default_notification")

