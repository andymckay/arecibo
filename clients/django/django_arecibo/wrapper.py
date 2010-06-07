from arecibo import post as error 
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.middleware.common import _is_ignorable_404
from socket import gethostname

import traceback
import sys
import time 

def post(request, status, **kw):
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
        data.extend( [ "    %s: %s" % (k, v) for k, v in request.POST.items() ])
        data.extend( [ "    %s: %s" % (k, v) for k, v in request.FILES.items() ])
        
    # build out data to send to Arecibo some fields (like timestamp)
    # are automatically added
    data = {
        "account": settings.ARECIBO_PUBLIC_ACCOUNT_NUMBER,
        "url": request.build_absolute_uri(), 
        "ip": request.META.get('REMOTE_ADDR'),
        "traceback": "\n".join(traceback.format_tb(exc_info[2])),
        "request": "\n".join(data).encode("utf-8"),
        "type": str(exc_info[0].__name__),
        "msg": str(exc_info[1]),
        "status": status,
        "uid": time.time(),
        "user_agent": request.META.get('HTTP_USER_AGENT'),     
    }

    data.update(kw)
    
    # it could be the site does not have the standard django auth
    # setup and hence no reques.user
    try:
        data["username"] = request.user.username, 
        # this will be "" for Anonymous
    except AttributeError:
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
    if not data.get("priority"):
        if status == 500: data["priority"] = 1
        else: data["priority"] = 5

    # populate my arecibo object
    err = error()
    for key, value in data.items():
        err.set(key, value)
        
    try:
        if getattr(settings, "ARECIBO_TRANSPORT", "") == "smtp":
            # use Djangos builtin mail 
            send_mail("Error", err.as_json(), 
                settings.DEFAULT_FROM_EMAIL,  
                [settings.ARECIBO_SERVER_EMAIL,])
        else:
            err.server(url=settings.ARECIBO_SERVER_URL)       
            err.send()
    except:
        # if you want this to be an explicit fail swap
        # change the comments on the next two lines around
        raise
        #pass
        
    return data["uid"]
      
