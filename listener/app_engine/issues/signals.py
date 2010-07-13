import django.dispatch

issue_created = django.dispatch.Signal(providing_args=["instance",])
comment_created = django.dispatch.Signal(providing_args=["instance",])
