# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Zone(models.Model):
    name = models.CharField(max_length=25)
    zip = models.CharField(max_length=8)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    precipitation = models.FloatField(default=0.0)
    ambient_temperature = models.FloatField(default=0.0)
