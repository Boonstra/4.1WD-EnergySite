from django.db import models


class Device(models.Model):
    brand = models.CharField(max_length=80)
    model = models.CharField(max_length=80)


class Category(models.Model):
    device = models.ForeignKey(Device)
    category = models.CharField(max_length=80)