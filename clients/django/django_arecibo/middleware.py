from django.http import Http404
from wrapper import post

class AreciboMiddleware(object):
    def process_exception(self, request, exception):
        """ This is middleware to process a request 
        and pass the value off to Arecibo. """
        # we keep the 404 check in there case
        if isinstance(exception, Http404):
            post(request, 404)
        else:
            # do we need to be finer grained on the exception status?
            post(request, 500)