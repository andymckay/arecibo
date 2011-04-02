from django.conf import settings

class Middleware:
    def process_request(self, request):
        request.view_access = (settings.ANONYMOUS_ACCESS or
                               request.user.is_authenticated())
        request.edit_access = request.user.is_authenticated()