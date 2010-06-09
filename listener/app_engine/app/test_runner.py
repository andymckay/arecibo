import os

from django.conf import settings
from django.test.simple import DjangoTestSuiteRunner

os.environ['SERVER_SOFTWARE'] = "Development"
settings.DATABASES['default']['SUPPORTS_TRANSACTIONS'] = True
# amongst other things this will suppress those annoying logs
settings.DEBUG = False

class AreciboRunner(DjangoTestSuiteRunner):
    pass