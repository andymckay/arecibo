from datetime import datetime

from django.http import HttpResponse
from django.conf import settings

from error.models import Error
from error.validations import valid_status
from urlparse import urlparse, urlunparse
from email.Utils import parsedate

def populate(err, incoming):
    """ Populate the error table with the incoming error """
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
        priority = int(incoming.get("priority", 0))
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