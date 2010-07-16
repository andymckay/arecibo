import django.dispatch

issue_created = django.dispatch.Signal(providing_args=["instance",])
comment_created = django.dispatch.Signal(providing_args=["instance",])

issue_status_changed = django.dispatch.Signal(providing_args=["instance", "old", "new"])
issue_assigned_changed = django.dispatch.Signal(providing_args=["instance", "old", "new"])
issue_priority_changed = django.dispatch.Signal(providing_args=["instance", "old", "new"])

issue_changed = django.dispatch.Signal(providing_args=["instance", "old"])
