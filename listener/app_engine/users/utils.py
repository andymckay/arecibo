from appengine_django.auth.models import User

def approved_users():
    return User.all().filter("is_staff = ", True)
