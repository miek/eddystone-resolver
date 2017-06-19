from django.core.management.base import BaseCommand
from eddystone_resolver.models import Beacon

class Command(BaseCommand):
    help = 'Generate EIDs for registered beacons'

    def handle(self, *args, **options):
        for beacon in Beacon.objects.all():
            beacon.eid_set.get_or_create(clock=beacon.counter_prev())
            beacon.eid_set.get_or_create(clock=beacon.counter())
            beacon.eid_set.get_or_create(clock=beacon.counter_next())
