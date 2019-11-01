from django.db import models
from users.models import CustomUser
from django.core.validators import RegexValidator


class Controller(models.Model):
    name = models.CharField(max_length=25)
    is_active = models.BooleanField(default=False)
    token = models.CharField(max_length=10, unique=True)

    owner = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.name
