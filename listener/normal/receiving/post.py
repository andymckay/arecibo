from datetime import datetime
from urlparse import urlparse, urlunparse

from django.conf import settings

from app.utils import break_url
from app.errors import StatusDoesNotExist
from error.models import Error
from error.validations import valid_status
from email.Utils import parsedate

from celery.task import task

@task(rate_limit='10/s')
def populate(incoming):
    """ Populate the error table with the incoming error """
    # special lookup the account
    err = Error()
    uid = incoming.get("account", "")
    if not settings.ANONYMOUS_POSTING:
        if not uid:
            raise ValueError, "Missing the required account number."

        if str(uid) != settings.ARECIBO_PUBLIC_ACCOUNT_NUMBER:
            raise ValueError, "Account number does not match"

    # special
    if incoming.has_key("url"):
        for k, v in break_url(incoming["url"]).items():
            setattr(err, k, v)

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
            setattr(err, dest, str(actual))

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
    if "timestamp" in incoming:
        tmstmp = incoming["timestamp"].strip()
        if tmstmp.endswith("GMT"):
            tmstmp = tmstmp[:-3] + "-0000"
        tme = parsedate(tmstmp)
        if tme:
            try:
                final = datetime(*tme[:7])
                err.error_timestamp = final
                err.error_timestamp_date = final.date()
            except ValueError, msg:
                err.errors += 'Date error on the field "%s", ignored.\n' % msg

    err.timestamp = datetime.now()
    err.timestamp_date = datetime.now().date()
    if "count" in incoming:
        err.count = incoming["count"]
    err.save()
