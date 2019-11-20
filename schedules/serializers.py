from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
from .models import Schedule


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Schedule
        fields = (
            'id',
            'period',
            'controller',
            'url'
        )


class SchedulesFromController(serializers.HyperlinkedModelSerializer):
    schedules = models.ListField()
    zone_active = models.CharField()

    class Meta:
        model = Schedule
        fields = (
            'controller',
            'schedules',
            'zone_active'
        )
