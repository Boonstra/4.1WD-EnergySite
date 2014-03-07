from django.db import models
from devices.models import Device
from facilities.models import Facility


class Time(models.Model):
    time = models.CharField(max_length=80)


class Measurement(models.Model):
    facility = models.ForeignKey(Facility)
    device = models.ForeignKey(Device)
    date = models.DateField()
    time = models.ForeignKey(Time)
    value = models.FloatField()