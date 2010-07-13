from userstorage.utils import activate, deactivate

class UserStorage:
    def process_request(self, request):
        activate(request)

    def process_response(self, request, response):
        deactivate(request)
        return response
