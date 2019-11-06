from django.db import models
from controllers.models import Controller
from modules.models import Module
from zones.models import Zone

class ActuatorsMeasurement(models.Model):
    water_consumption = models.FloatField(default=0.0)
    reservoir_level = models.FloatField(default=0.0)
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE)


class ModulesMeasurement(models.Model):
    temperature = models.FloatField(default=0.0)
    ground_humidity = models.IntegerField(default=0)
    battery_level = models.IntegerField(default=0)

    module = models.ForeignKey(Module, on_delete=models.CASCADE)

class ZoneMeasurement(models.Model):
    soil_temperature = models.FloatField(default=0.0)
    air_temperature = models.FloatField(default=0.0)
    precipitation = models.FloatField(default=0.0)

    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)