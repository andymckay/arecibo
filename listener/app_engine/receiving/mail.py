from django.utils.simplejson import loads, dumps
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from error.models import Error

from app.utils import _pdb, log
from google.appengine.api import mail
from receiving.post import populate

def parse(content_type, body):
    data = body.decode()
    if data.rfind("}") > 0:
        # strip out any crap on the end
        end = data.rfind("}")
        # not sure why i was doing this, i'm sure there
        # was a good reason at one point
        text = data[:end] + "}"
        err = Error()
        json = loads(text, strict=False)
        populate(err, json)
        return True

def post(request):
    """ Add in a post """
    log("Processing email message") 
    mailobj = mail.InboundEmailMessage(request.raw_post_data)
    found = False
    
    for content_type, body in mailobj.bodies("text/plain"): 
        found = parse(content_type, body)
    for content_type, body in mailobj.bodies("text/html"): 
        found = parse(content_type, body)
        
    if not found:
        log("No contents found in the message.")

    return HttpResponse("message parsed")