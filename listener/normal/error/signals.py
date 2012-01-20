import django.dispatch

error_created = django.dispatch.Signal(providing_args=["instance",])
group_created = django.dispatch.Signal(providing_args=["instance",])
group_assigned = django.dispatch.Signal(providing_args=["instance",])
error_assigned = django.dispatch.Signal(providing_args=["instance",])
