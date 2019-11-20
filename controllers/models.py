from django.db import models
from users.models import CustomUser
from django.core.validators import RegexValidator


class Controller(models.Model):
    name = models.CharField(max_length=25)
    is_active = models.BooleanField(default=False, blank=True)
    token = models.CharField(max_length=10, unique=True, primary_key=True)
    status = models.BooleanField(default=False, blank=True)
    read = models.BooleanField(default=True, blank=True)
    timer = models.IntegerField(default=0.0, blank=True)

    owner = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.name


class ControllerSpecification(models.Model):
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, null=False, blank=False)

    def __str__(self):
        return self.name
