from django.utils.thread_support import currentThread

_active = {}

def activate(request):
    if request and request.user:
        _active[currentThread()] = request.user

def deactivate(request):
    global _active
    if currentThread() in _active:
        del _active[currentThread()]

def get_user():
    if currentThread() not in _active:
        return None
    return _active[currentThread()]
