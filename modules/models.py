from django.db import models
from controllers.models import Controller


class Module(models.Model):
    rf_address = models.IntegerField(unique=True)
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE)

    def __str__(self):
        return self.rf_address
