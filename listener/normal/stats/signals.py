import django.dispatch

stats_completed = django.dispatch.Signal(providing_args=["instance",])
