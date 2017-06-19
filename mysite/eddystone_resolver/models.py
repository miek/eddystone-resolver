import binascii

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from eddystone_resolver.crypto import compute_eid

class Beacon(models.Model):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=32)
    reg_time = models.DateTimeField()
    reg_counter = models.IntegerField()
    k = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

    def counter(self, t=timezone.now()):
        diff = int((t - self.reg_time).total_seconds())
        c = (self.reg_counter + diff) & 0xFFFFFFFF
        c = (c >> self.k) << self.k
        return c

    def counter_roll(self):
        return (1 << self.k)

    def counter_prev(self, t=timezone.now()):
        return (self.counter(t) - self.counter_roll()) & 0xFFFFFFFF

    def counter_next(self, t=timezone.now()):
        return (self.counter(t) + self.counter_roll()) & 0xFFFFFFFF

class EID(models.Model):
    beacon = models.ForeignKey(Beacon, on_delete=models.CASCADE)
    eid = models.CharField(max_length=16)
    clock = models.IntegerField()

    def __str__(self):
        return self.eid

@receiver(pre_save, sender=EID)
def generate_eid(sender, instance, *args, **kwargs):
    eid_bytes = compute_eid(instance.beacon.key, instance.beacon.k, instance.clock)
    instance.eid = binascii.hexlify(eid_bytes).decode("ascii")
