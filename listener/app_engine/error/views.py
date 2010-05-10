from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.simple import direct_to_template
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from error.models import Error
from error.validations import valid_status
from app.errors import StatusDoesNotExist

from email.Utils import parsedate
from datetime import datetime
from urlparse import urlparse, urlunparse

@user_passes_test(lambda u: u.is_staff)
def errors_list(request):
    page = Error.all().order_by("-timestamp")
    return direct_to_template(request, "list.html", extra_context={"page":page})

@user_passes_test(lambda u: u.is_staff)
def error_view(request, id):
    error = Error.get(id)
    return direct_to_template(request, "view.html", extra_context={"error":error})

###################################################################################################
# this is the bit that does the posting

def post(request):
    """ Add in a post """ 
    err = Error()
    err.ip = request.META.get("REMOTE_ADDR", "")
    err.user_agent = request.META.get("HTTP_USER_AGENT", "")

    populate(err, request.POST)
    return HttpResponse("Error recorded")
    
def populate(err, incoming):
    # special lookup the account    
    uid = incoming.get("account", "")
    if not uid:
        raise ValueError, "Missing the required account number."
    if str(uid) != settings.ARECIBO_PUBLIC_ACCOUNT_NUMBER:
        raise ValueError, "Account number does not match"
            
    # special
    if incoming.has_key("url"):
        err.raw = incoming["url"]
        parsed = list(urlparse(incoming["url"]))
        err.protocol, err.domain = parsed[0], parsed[1]
        err.query = urlunparse(["",""] + parsed[2:])

    # check the status codes
    if incoming.has_key("status"):
        status = str(incoming["status"])
        try:
            valid_status(status)
            err.status = status
        except StatusDoesNotExist:
            err.errors += "Status does not exist, ignored.\n"

    # not utf-8 encoded
    for src, dest in [
        ("ip", "ip"),
        ("user_agent", "user_agent"),
        ("uid", "uid"),
        ]:
        actual = incoming.get(src, None)
        if actual is not None:
            setattr(err, dest, actual)

    try:
        priority = int(incoming["priority"] or 0)
    except ValueError:
        priority = 0
    err.priority = min(priority, 10)

    # possibly utf-8 encoding            
    for src, dest in [
        ("type", "type"),
        ("msg", "msg"),
        ("server", "server"),
        ("traceback", "traceback"),                        
        ("request", "request"),                        
        ("username", "username")
        ]:
        actual = incoming.get(src, None)
        if actual is not None:
            try:
                setattr(err, dest, actual.encode("utf-8"))
            except UnicodeDecodeError:
                err.errors += "Encoding error on the %s field, ignored.\n" % src
    
    # timestamp handling
    if incoming.has_key("timestamp"):
        tmstmp = incoming["timestamp"].strip()
        if tmstmp.endswith("GMT"):
            tmstmp = tmstmp[:-3] + "-0000"
        tme = parsedate(tmstmp)
        if tme:
            try:
                final = datetime(*tme[:7])
                err.error_timestamp = final
            except ValueError, msg:
                err.errors += 'Date error on the field "%s", ignored.\n' % msg
    
    err.timestamp = datetime.now()
    err.save()
