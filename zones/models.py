from __future__ import unicode_literals
from controllers.models import Controller
from django.db import models

class Zone(models.Model):
    name = models.CharField(max_length=25)
    zip = models.CharField(max_length=8)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=False)
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE)
