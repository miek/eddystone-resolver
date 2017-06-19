from django.core.management.base import BaseCommand, CommandError
from eddystone_resolver.models import Beacon, EID

class Command(BaseCommand):
    help = 'Generate EIDs for registered beacons'

    def handle(self, *args, **options):
        self.stdout.write("hi")
