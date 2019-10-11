from django.db import models
from controllers.models import Controller


class Module(models.Model):
    rf_address = models.CharField(max_length=30, unique=True)

    controller = models.ForeignKey(Controller, on_delete=models.CASCADE)
