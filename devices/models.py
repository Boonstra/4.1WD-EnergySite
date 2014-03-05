from django.db import models
from facilities.models import Facility


class Device(models.Model):
    facilities = models.ManyToManyField(Facility)
    brand = models.CharField(max_length=80)
    model = models.CharField(max_length=80)


class Category(models.Model):
    device = models.ForeignKey(Device)
    category = models.CharField(max_length=80)