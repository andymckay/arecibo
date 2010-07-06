# add in a user created signal
import django.dispatch

user_created = django.dispatch.Signal(providing_args=["instance",])