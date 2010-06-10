from django.core.management.base import BaseCommand, CommandError

import code
import getpass
import sys
import os

from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.ext import db

def auth_func():
    return raw_input('Username:'), getpass.getpass('Password:')

class Command(BaseCommand):
    help = 'Command shell for the remote App Engine instance'
    
    def handle(self, *args, **options):
        app_id = os.environ.get("APPLICATION_ID")
        host = "%s.appspot.com" % app_id
        remote_api_stub.ConfigureRemoteDatastore(app_id, '/remote_api', auth_func, host)
        code.interact('App Engine interactive console for %s' % (app_id,), None, locals())