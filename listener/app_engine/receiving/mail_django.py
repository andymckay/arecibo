# # this is a specific handler for django
import re
from urlparse import urlunparse

from django.conf import settings

from app.utils import log, render_plain
from google.appengine.api import mail
from receiving.post import populate
from error.models import Error

mapping_404_key = {
    "Referrer":"request",
    "Requested URL":"url",
    "User agent":"user_agent",
    "IP address":"ip"
}

mapping_404_value = {
    "request": "HTTP_REFERER: %s"
}

mapping_500_key = {
    "server": re.compile("'SERVER_NAME.*'(?P<value>.*?)'"),
    "user_agent": re.compile("'HTTP_USER_AGENT.*'(?P<value>.*?)'"),
    "ip": re.compile("'REMOTE_ADDR.*'(?P<value>.*?)'"),
    "path": re.compile("'PATH_INFO.*'(?P<value>.*?)'"),
    "host": re.compile("'HTTP_HOST.*'(?P<value>.*?)'"),
    "query_string": re.compile("'QUERY_STRING.*'(?P<value>.*?)'"),
    "server_port": re.compile("'SERVER_PORT.*'(?P<value>.*?)'"),
    "server_protocol": re.compile("'SERVER_PROTOCOL.*'(?P<value>.*?)'"),
}

def parse_http(value):
    return "%s" % value.split('/')[0].lower()

mapping_500_value = {
    "server_protocol": parse_http
}

def parse_404(body, subject):
    domain = subject.split(" on ")[-1]
    body = body.decode().replace("=\n", "")
    lines = body.split("\n")
    data = {"status": 404, "priority": 5}
    for line in lines:
        if not line: continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value == "None": value = None
        key = mapping_404_key.get(key)
        if key in mapping_404_value:
            value = mapping_404_value[key] % value
        data[key] = value
    try:
        data["url"] = "http://%s%s" % (domain, data["url"])
        # note we have to assume this
    except KeyError:
        pass
    return data

def parse_500(body, subject):
    # subject is not needed
    data = {"traceback":[], "request":[], "status": 500, "priority": 1}
    data["traceback"], data["request"] = body.decode().split("\n\n<")
    for key, regex in mapping_500_key.items():
        match = regex.search(data["request"])
        if match:
            value = match.groups()[0]
            if key in mapping_500_value:
                value = mapping_500_value[key](value)
            data[key] = value
    try:
        data["url"] = urlunparse((
            data["server_protocol"], data["host"],
            data["path"], data["query_string"],
            "", "")
            )
    except KeyError:
        pass
    try:
        data["type"], data["message"] = data["traceback"].strip().split("\n")[-1].split(": ", 2)
    except ValueError:
        pass
    return data

def post(request):
    """ Add in a post """
    log("Processing email message")
    mailobj = mail.InboundEmailMessage(request.raw_post_data)
    to = mailobj.to
    key = to.split("-", 1)[1].split("@")[0]
    if key != settings.ARECIBO_PUBLIC_ACCOUNT_NUMBER:
        log("To address does not match account number")
        return
    
    for content_type, body in mailobj.bodies("text/plain"):
        if mailobj.subject.find(" Broken ") > -1:
            log("Trying to parse body using 404 parser")
            result = parse_404(body, mailobj.subject)
        else:
            log("Trying to parse body using 500 parser")
            result = parse_500(body, mailobj.subject)
        err = Error()
        result["account"] = key
        populate(err, result)
    
    return render_plain("message parsed")