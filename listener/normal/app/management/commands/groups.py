from django.core.management.base import BaseCommand

from error.models import Error
from error.models import Group
from error.signals import error_created

class Command(BaseCommand):
    help = 'Drops groups and then refires signals on addons, recreating the groups'

    def handle(self, *args, **options):
        groups = Group.objects.all()
        print 'Deleting %s group(s)' % groups.count()
   	groups.delete()

        for error in Error.objects.all():
            error_created.send(sender=Error, instance=error)        
