from arecibo import post as error
from django.conf import settings
from django.core.mail import send_mail
from django.middleware.common import _is_ignorable_404

import traceback
import sys
import time

NO_DEFAULT = object()
def arecibo_setting(key, default=NO_DEFAULT):
    arecibo_settings = getattr(settings, 'ARECIBO_SETTINGS', {})
    if default is NO_DEFAULT:
        return arecibo_settings[key]
    return arecibo_settings.get(key, default)

def exclude_post_var(name):
    return check_exclusions(arecibo_setting('EXCLUDED_POST_VARS', ()), name)

def exclude_file(name):
    return check_exclusions(arecibo_setting('EXCLUDED_FILES', ()), name)

def check_exclusions(exclusions, name):
    return name in exclusions

def filter_post_var(name, value, mask_char='*'):
    filters = arecibo_setting('FILTERED_POST_VARS', ())
    if not name in filters:
        return name, value
    return name, mask_char[0] * len(value)

def filter_file(name, value, mask_char='*'):
    filters = arecibo_setting('FILTERED_FILES', ())
    if not name in filters:
        return name, value

    return name, mask_chars[0] * len(name)

class DjangoPost:
    def __init__(self, request, status, **kw):
        # first off, these items can just be ignored, we
        # really don't care about them too much
        path = request.get_full_path()
        if _is_ignorable_404(path):
            return

        # if you've set INTERNAL_IPS, we'll respect that and
        # ignore any requests, we suggest settings this so your
        # unit tests don't blast the server
        if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return

        exc_info = sys.exc_info()
        items = ['HOME', 'HTTP_ACCEPT', 'HTTP_ACCEPT_ENCODING', 'HTTP_REFERER', \
                 'HTTP_ACCEPT_LANGUAGE', 'HTTP_CONNECTION', 'HTTP_HOST', 'LANG', \
                 'PATH_INFO', 'QUERY_STRING', 'REQUEST_METHOD', 'SCRIPT_NAME', \
                 'SERVER_NAME', 'SERVER_PORT', 'SERVER_PROTOCOL', 'SERVER_SOFTWARE']
        data = [ "%s: %s" % (k, request.META[k]) for k in items if request.META.get(k)]
        if request.method.lower() == "post":
            data.append("POST and FILES Variables:")
            data.extend( [ "    %s: %s" % filter_post_var(k, v) for k, v in request.POST.items() if not exclude_post_var(k) ])
            data.extend( [ "    %s: %s" % filter_file(k, v) for k, v in request.FILES.items() if not exclude_file(k) ])

        # build out data to send to Arecibo some fields (like timestamp)
        # are automatically added
        self.data = {
            "account": getattr(settings, 'ARECIBO_PUBLIC_ACCOUNT_NUMBER', ''),
            "url": request.build_absolute_uri(),
            "ip": request.META.get('REMOTE_ADDR'),
            "traceback": "\n".join(traceback.format_tb(exc_info[2])),
            "request": "\n".join(data).encode("utf-8"),
            "type": exc_info[0],
            "msg": str(exc_info[1]),
            "status": status,
            "uid": time.time(),
            "user_agent": request.META.get('HTTP_USER_AGENT'),
        }

        # we might have a traceback, but it's not required
        try:
            if self.data["type"]:
                self.data["type"] = str(self.data["type"].__name__)
        except AttributeError:
            pass

        self.data.update(kw)

        # it could be the site does not have the standard django auth
        # setup and hence no request.user
        try:
            self.data["username"] = request.user.username,
            # this will be "" for Anonymous
        except Exception:
            pass

        # a 404 has some specific formatting of the error that can be useful
        if status == 404:
            msg = ""
            for m in exc_info[1]:
                if isinstance(m, dict):
                    tried = "\n".join(m["tried"])
                    msg = "Failed to find %s, tried: \n%s" % (m["path"], tried)
                else:
                    msg += m
            data["msg"] = msg

        # if we don't get a priority, lets create one
        if not self.data.get("priority"):
            if status == 500: self.data["priority"] = 1
            else: self.data["priority"] = 5

        # populate my arecibo object
        self.err = error()
        for key, value in self.data.items():
            self.err.set(key, value)

    def send(self):
        try:
            if getattr(settings, "ARECIBO_TRANSPORT", "") == "smtp":
                # use Djangos builtin mail
                send_mail("Error", self.err.as_json(),
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ARECIBO_SERVER_EMAIL,])
            else:
                self.err.server(url=settings.ARECIBO_SERVER_URL)
                self.err.send()
        except Exception, e:
            # if you want this to be an explicit fail swap
            # change the comments on the next two lines around
            print "Hit an exception sending: {e}"
            #raise
            pass


def post(request, status, **kw):
    obj = DjangoPost(request, status, **kw)
    obj.send()
    return obj.data.get("uid")
