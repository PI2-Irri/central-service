from django.db import models
from zones.models import Zone


class Schedule(models.Model):
    schedule = models.DateTimeField()
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
