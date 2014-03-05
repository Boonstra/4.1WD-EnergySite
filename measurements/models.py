from django.db import models
from devices.models import Device


class Measurement(models.Model):
    device = models.ForeignKey(Device)
    datetime = models.DateTimeField()
    value = models.IntegerField()


class Time(models.Model):
    time = models.CharField(max_length=80)