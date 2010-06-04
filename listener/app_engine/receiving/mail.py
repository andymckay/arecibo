from django.utils.simplejson import loads

from django.http import HttpResponse

from error.models import Error

from app.utils import _pdb, log
from google.appengine.api import mail
from receiving.post import populate

def post(request):
    """ Add in a post """ 
    mailobj = mail.InboundEmailMessage(request.raw_post_data)
    mailobj.bodies("text/plain")
    found = False
    for content_type, body in mailobj.bodies("text/plain"): 
        data = body.decode()
        if data.rfind("}") > 0:
            # strip out any crap on the end
            end = data.rfind("}")
            # not sure why i was doing this, i'm sure there
            # was a good reason at one point
            text = data[:end] + "}"
            try:
                err = Error()
                populate(err, loads(text, strict=False))            
            except (ValueError, ObjectDoesNotExist):
                import sys
                errtype, errvalue = sys.exc_info()[:2]
                log("Failed to parse email, contents: %s, reason: %s, %s" % (text[:-1][:50], errtype, errvalue))

            found = True
            break

    if not found:
        log("No contents found in the message.")

    return HttpResponse("message parsed")