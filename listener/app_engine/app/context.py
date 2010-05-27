from urllib import urlencode

def context(request):
    data = {}
    data["user"] = request.user
    
    ignore = ["page",]
    qs = request.GET.copy()
    if "page" in qs:
        del qs["page"]

    data["qs"] = ""
    if qs:
        data["qs"] = "%s" % urlencode(qs)
    
    return data