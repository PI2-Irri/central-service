from __future__ import unicode_literals
from controllers.models import Controller
from django.db import models

class Zone(models.Model):
    name = models.CharField(max_length=25)
    zip = models.CharField(max_length=9)
    latitude = models.FloatField(default=0.0, blank=True, null=False)
    longitude = models.FloatField(default=0.0, blank=True, null=False)
    location = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False, blank=True)
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE)
