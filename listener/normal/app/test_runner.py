import os

from django.conf import settings
from django.test.simple import DjangoTestSuiteRunner

from django.core import mail
from django.core.mail.backends import locmem

from django.core.mail.message import EmailMessage


# amongst other things this will suppress those annoying logs
settings.DEBUG = False


class AreciboRunner(DjangoTestSuiteRunner):
    def setup_test_environment(self, **kwargs):
        msgs = 'django.contrib.messages.context_processors.messages'
        if msgs not in settings.TEMPLATE_CONTEXT_PROCESSORS:
            tcp = list(settings.TEMPLATE_CONTEXT_PROCESSORS)
            tcp.append(msgs)
            settings.TEMPLATE_CONTEXT_PROCESSORS = tuple(tcp)
        settings.DEBUG_PROPAGATE_EXCEPTIONS = True
        settings.CELERY_ALWAYS_EAGER = True
        super(AreciboRunner, self).setup_test_environment(**kwargs)
