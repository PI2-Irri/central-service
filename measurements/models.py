from django.db import models
from controllers.models import Controller


class ActuatorsMeasurement(models.Model):
    water_consumption = models.FloatField(default=0.0)
    reservoir_level = models.FloatField(default=0.0)

    controller = models.ForeignKey(Controller, on_delete=models.CASCADE)
