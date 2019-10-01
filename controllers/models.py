from django.db import models


class Controller(models.Model):
    name = models.CharField(max_length=25)
    is_valid = models.BooleanField(default=False)
    token = models.CharField(max_length=10, unique=True)
