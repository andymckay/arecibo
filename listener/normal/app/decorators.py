from django.contrib.auth.decorators import user_passes_test
from django.conf import settings


def arecibo_login_required(func):
    return user_passes_test(lambda u: settings.ANONYMOUS_ACCESS or u.is_staff)(func)