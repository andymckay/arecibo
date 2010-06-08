from exceptions import Exception

class StatusDoesNotExist(Exception): pass

from django.template import RequestContext, loader
from django.http import HttpResponse

def not_found_error(request):                     
    t = loader.get_template('404.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c), status=404)
    
def application_error(request):                     
    t = loader.get_template('500.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c), status=500)