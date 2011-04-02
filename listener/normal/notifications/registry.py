_registry = {}

def register(klass, name):
    global _registry
    _registry[name] = klass
    
def get():
    return _registry