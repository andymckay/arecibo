# general utils
import logging
from django.conf import settings
from django.http import HttpResponseRedirect

try:
    from functools import update_wrapper, wraps
except ImportError:
    from django.utils.functional import update_wrapper, wraps  # Python 2.3, 2.4 fallback.

def log(msg):
    logging.info(" Arecibo: %s" % msg)

def safe_int(key, result=None):
    try:
        return int(key)
    except (ValueError, AttributeError):
        return result

def safe_string(text, result=""):
    try:
        return str(text)
    except (ValueError, AttributeError):
        return result

def has_private_key(view_func):
    """ Will check that the person accessing the page is doing so with the private URL """
    def wrapper(*args, **kwargs):
        request = args[0]
        if settings.ARECIBO_PRIVATE_ACCOUNT_NUMBER not in request.get_full_path().split("/"):
            return HttpResponseRedirect(settings.LOGIN_URL)
        return view_func(*args, **kwargs)
    return wraps(view_func)(wrapper)

def _pdb():
    import pdb, sys
    sys.__stdout__.write('\a')
    sys.__stdout__.flush()
    debugger = pdb.Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__)
    debugger.set_trace()