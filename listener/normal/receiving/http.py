from django.http import HttpResponse
from django.views.decorators.csrf import csrf_response_exempt

from app.utils import render_plain
from error.models import Error
from receiving.post import populate


def post(request):
    """ Add in a post """
    err = Error()
    err.ip = request.META.get("REMOTE_ADDR", "")
    err.user_agent = request.META.get("HTTP_USER_AGENT", "")

    populate(err, request.POST)
    return render_plain("Error recorded")
