from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=255, unique=True)

    registration_date = models.DateTimeField(null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    is_trusty = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name'
    ]
