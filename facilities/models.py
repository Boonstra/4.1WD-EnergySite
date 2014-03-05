from django.db import models


class Facility(models.Model):
    street = models.CharField(max_length=80)
    street2 = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    zipcode = models.CharField(max_length=80)
    inhabitants = models.IntegerField()
    email = models.CharField(max_length=80)
    phone_number = models.CharField(max_length=80)
    password = models.CharField(max_length=256)