# general utils
import logging
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.utils.encoding import smart_unicode
from django.core.urlresolvers import reverse

from urlparse import urlparse, urlunparse

try:
    from functools import update_wrapper, wraps
except ImportError:
    from django.utils.functional import update_wrapper, wraps  # Python 2.3, 2.4 fallback.

def log(msg):
    if settings.DEBUG:
        logging.info(" Arecibo: %s" % msg)

def safe_int(key, result=None):
    try:
        return int(key)
    except (ValueError, AttributeError):
        return result

def render_plain(msg):
    return HttpResponse(msg, mimetype="text/plain")

def render_json(view_func):
    def wrapper(*args, **kwargs):
        data = view_func(*args, **kwargs)
        return HttpResponse(simplejson.dumps(data), mimetype='application/json')
    return wrapper

def not_allowed(request):
    return HttpResponseRedirect(reverse("not-allowed"))

def safe_string(text, result=""):
    try:
        return str(text)
    except (ValueError, AttributeError):
        return result

def trunc_string(text, length, ellipsis="..."):
    if len(text) < length:
        return text
    else:
        return "%s%s" % (text[:length-len(ellipsis)], ellipsis)

def has_private_key(view_func):
    """ Will check that the person accessing the page is doing so with the private URL """
    def wrapper(*args, **kwargs):
        request = args[0]
        if settings.ARECIBO_PRIVATE_ACCOUNT_NUMBER not in request.get_full_path().split("/"):
            return HttpResponseRedirect(settings.LOGIN_URL)
        return view_func(*args, **kwargs)
    return wraps(view_func)(wrapper)

def break_url(url):
    result = {"raw": url}
    parsed = list(urlparse(url))
    result["protocol"] = parsed[0]
    result["domain"] = parsed[1]
    result["query"] = urlunparse(["",""] + parsed[2:])
    return result

def _pdb():
    import pdb, sys
    sys.__stdout__.write('\a')
    sys.__stdout__.flush()
    debugger = pdb.Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__)
    debugger.set_trace()
