from django.db import models
from facilities.models import Facility


class Category(models.Model):
    category = models.CharField(max_length=80)


class Device(models.Model):
    facilities = models.ManyToManyField(Facility)
    category = models.ForeignKey(Category)
    brand = models.CharField(max_length=80)
    model = models.CharField(max_length=80)