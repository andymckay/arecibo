# this requires Django to get at the settings
# not sure what other apps do for thi
from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson
from django.middleware.common import _is_ignorable_404

from google.appengine.api import urlfetch
from google.appengine.api import mail

from urllib import urlencode
from urlparse import urljoin, urlparse, urlunparse

import logging
import traceback
import sys
import time 

def get_host(request):
    """Returns the HTTP host using the environment or request headers."""
    # We try three options, in order of decreasing preference.
    if 'HTTP_X_FORWARDED_HOST' in request.META:
        host = request.META['HTTP_X_FORWARDED_HOST']
    elif 'HTTP_HOST' in request.META:
        host = request.META['HTTP_HOST']
    else:
        # Reconstruct the host using the algorithm from PEP 333.
        host = request.META['SERVER_NAME']
        server_port = request.META['SERVER_PORT']
        if server_port != (request.is_secure() and 443 or 80):
            host = '%s:%s' % (host, server_port)
    return host
    
def getpath(request):
    location = request.get_full_path()
    if not ':' in location:
        current_uri = '%s://%s%s' % (request.is_secure() and 'https' or 'http',
                    get_host(request), request.path)
        location = urljoin(current_uri, location)
    return location

def post(request, status, **kw):
    exc_info = sys.exc_info() 

    path = request.get_full_path()
    if _is_ignorable_404(path):
        return
    
    if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
        return
        
    data = {
        "account": settings.ARECIBO_PUBLIC_ACCOUNT_NUMBER,
        "url": getpath(request),
        "ip": request.META.get('REMOTE_ADDR'),
        "traceback": "\n".join(traceback.format_tb(exc_info[2])),
        "type": str(exc_info[0].__name__),
        "msg": str(exc_info[1]),
        "status": status,
        "uid": time.time(),
        "user_agent": request.META.get('HTTP_USER_AGENT'),
        "server": "Google App Engine"     
    }

    # it could be the site does not have the standard django auth
    # setup and hence no reques.user
    try:
        data["username"] = request.user.username, 
        # this will be "" for Anonymous
    except AttributeError:
        pass

    data.update(kw)
            
    # a 404 has some specific formatting of the error that
    # can be useful
    if status == 404:
        msg = ""
        for m in exc_info[1]:                             
            tried = "\n".join(m["tried"])
            msg = "Failed to find %s, tried: \n\t%s" % (m["path"], tried)
        data["msg"] = msg
                                                                   
    # if we don't get a priority, make create one   
    if not data.get("priority"):
        if status == 500:
            data["priority"] = 1
        else: 
            data["priority"] = 5
        
    try:
        if getattr(settings, "ARECIBO_TRANSPORT", None):
            try:
                sender = settings.ARECIBO_EMAIL_SENDER_ADDRESS
            except AttributeError:
                raise ValueError, "We must have a valid ARECIBO_EMAIL_SENDER_ADDRESS in the settings."

            mail.send_mail(
                sender=sender,
                to=settings.ARECIBO_SERVER_EMAIL,
                subject="Error",
                body=simplejson.dumps(data))
        else:                
            udata = urlencode(data)
            headers = {'Content-Type': 'application/x-www-form-urlencoded', "Accept": "text/plain"}
            url = list(urlparse(settings.ARECIBO_SERVER_URL))
            if url[2] != "/v/1/": url[2] = "/v/1/"
            result = urlfetch.fetch(
                url=urlunparse(url), 
                payload=udata, 
                method=urlfetch.POST, 
                headers=headers)

    except:
        raise
        # write to the standard google app engine log
        # http://code.google.com/appengine/docs/python/logging.html
        exctype, value = sys.exc_info()[:2]
        msg = "There was an error posting that error to Arecibo via smtp %s, %s" % (exctype, value)
        logging.error("Arecibo: %s", msg)
        
    return data["uid"]
      