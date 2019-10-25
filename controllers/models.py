from django.db import models
from users.models import CustomUser
from django.core.validators import RegexValidator


class Controller(models.Model):
    name = models.CharField(max_length=25)
    is_valid = models.BooleanField(default=False)
    ip_address = models.CharField(
        max_length=15,
        unique=True,
        default="0.0.0.0",
        validators=[
            RegexValidator(
                regex='^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$',
                message='Incorrect IP address format',
                code='invalid_ip_address'
            ),
    ])
    port = models.CharField(max_length=6, default=':3000/')

    token = models.CharField(max_length=10, unique=True)

    owner = models.ManyToManyField(CustomUser)
