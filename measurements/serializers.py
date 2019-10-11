from rest_framework import serializers
from .models import ActuatorsMeasurement
from .models import ModulesMeasurement

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

class ModulesMeasurementSerializer():

    class Meta:
        model = ModulesMeasurement
        fields = (
            'temperature',
            'ground_humidity',
            'battery_level',
            'is_active',
            'module',
        )