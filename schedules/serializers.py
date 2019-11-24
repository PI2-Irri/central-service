from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
from .models import Schedule


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Schedule
        fields = (
            'id',
            'zone',
            'schedule',
            'url'
        )


class SchedulesFromController(serializers.HyperlinkedModelSerializer):
    schedule = serializers.ListField(default=[])
    attr = serializers.JSONField()
    zone = serializers.CharField()

    class Meta:
        model = Schedule
        fields = (
            'zone',
            'attr',
            'schedule'
        )
