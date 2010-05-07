def context(request):
    data = {}
    data["user"] = request.user
    return data