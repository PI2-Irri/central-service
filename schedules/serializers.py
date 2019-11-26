from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
from .models import Schedule
from .models import Zone
from controllers.models import Controller
from datetime import datetime


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    zone_name = serializers.CharField()
    time = serializers.CharField()

    class Meta:
        model = Schedule
        fields = (
            'id',
            'zone_name',
            'time',
            'url'
        )

    def to_internal_value(self, data):
        if data.get('token') and data.get('zone_name') and data.get('time'):
            return data
        else:
            raise APIException(
                {'error': 'Invalid data sended.'}
            )

    def create(self, validated_data):

        try:
            controller = Controller.objects.get(
                token=validated_data.get('token')
            )

            zone = controller.zone_set.get(
                name=validated_data.get('zone_name')
            )

            schedule = Schedule.objects.get(
                zone=zone,
                schedule=datetime.strptime(
                    validated_data.get('time'),
                    '%Y-%m-%d %H:%M'
                )
            )

            exception = APIException(
                {'error': 'This schedule is just registered.'}
            )
            exception.status_code = 400

            raise exception
        except Schedule.DoesNotExist:
            schedule = Schedule.objects.create(
                zone=zone,
                schedule=datetime.strptime(
                    validated_data.get('time'),
                    '%Y-%m-%d %H:%M'
                )
            )

            exception = APIException(
                {
                    'zone': schedule.zone.name,
                    'schedule': schedule.schedule
                }
            )

            exception.status_code = 201

            raise exception
        except Zone.DoesNotExist:
            raise APIException(
                {'error': 'Name does not match with any controller zone name.'}
            )
        except Controller.DoesNotExist:
            raise APIException(
                {'error': 'Token does not match with any controller.'}
            )

        return schedule


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
