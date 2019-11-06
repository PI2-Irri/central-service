from rest_framework import serializers
from .models import ActuatorsMeasurement
from .models import ModulesMeasurement
from .models import ZoneMeasurement

class ActuatorsMeasurementSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ActuatorsMeasurement
        fields = (
            'id',
            'water_consumption',
            'reservoir_level',
            'is_active',
            'controller',
            'url'
        )


class ModulesMeasurementSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ModulesMeasurement
        fields = (
            'temperature',
            'ground_humidity',
            'battery_level',
            'module',
        )

class ZoneMeasurementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
            model = ZoneMeasurement
            fields = (
                'air_temperature',
                'precipitation',
                'ground_humidity',
                'status_modules'
            )