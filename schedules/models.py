from django.db import models
from zones.models import Zone
from users.models import CustomUser


class Schedule(models.Model):
    schedule = models.DateTimeField()
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

class Notification(models.Model):
    date = models.DateTimeField()
    message = models.CharField(default="", max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
