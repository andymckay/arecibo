from django.contrib.auth.decorators import user_passes_test
from django.conf import settings


def arecibo_login_required(func):
    if settings.ANONYMOUS_ACCESS:
        return user_passes_test(lambda u: True)(func)
    
    return user_passes_test(lambda u: u.is_staff)(func)