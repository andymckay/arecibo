from django.contrib.auth.models import User

def approved_users():
    return User.objects.filter(is_staff=True)
