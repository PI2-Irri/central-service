from rest_framework import serializers
from .models import ActuatorsMeasurement


class ActuatorsMeasurementSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ActuatorsMeasurement
        fields = (
            'id',
            'water_consumption',
            'reservoir_level',
            'controller',
            'url'
        )
