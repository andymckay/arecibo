import django.dispatch

notification_created = django.dispatch.Signal(providing_args=["instance",])