from urllib import urlencode
from django.conf import settings

def context(request):
    data = {}
    data["user"] = request.user
    data["public_key"] = settings.ARECIBO_PUBLIC_ACCOUNT_NUMBER
    data["private_key"] = settings.ARECIBO_PRIVATE_ACCOUNT_NUMBER
    data["site_url"] = settings.SITE_URL

    ignore = ["page",]
    qs = request.GET.copy()
    if "page" in qs:
        del qs["page"]

    data["qs"] = ""
    if qs:
        data["qs"] = "%s" % urlencode(qs)

    return data