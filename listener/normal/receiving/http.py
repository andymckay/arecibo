from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app.utils import render_plain
from error.models import Error
from receiving.post import populate


@csrf_exempt
def post(request):
    """ Add in a post """
    data = request.POST.copy()
    if "ip" not in data:
        data["ip"] = request.META.get("REMOTE_ADDR", "")
    if "user_agent" not in data:
        data["user_agent"] = request.META.get("HTTP_USER_AGENT", "")
    populate(data)#.delay(data)
    return render_plain("Error recorded")
