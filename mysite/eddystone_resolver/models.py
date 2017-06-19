from django.db import models

class Beacon(models.Model):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=32)
    reg_time = models.DateTimeField()
    reg_counter = models.IntegerField()
    k = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

class EID(models.Model):
    beacon = models.ForeignKey(Beacon, on_delete=models.CASCADE)
    eid = models.CharField(max_length=16)
    clock = models.IntegerField()

    def __str__(self):
        return self.eid
