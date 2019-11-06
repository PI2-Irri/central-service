from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
from .models import Controller
from .models import Zone


class ZoneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Zone
        fields = (
            'id',
            'name',
            'zip',
            'latitude',
            'longitude',
            'controller',
            'is_active',
            'url'
        )

    def to_internal_value(self, data):
        if isinstance(data.get('controller'), str):
            return data
        else:
            raise APIException(
                {'error': 'Token information has a invalid type.'}
            )

    def create(self, validated_data):
        token = validated_data.get('controller')
        zone = None

        if not token:
            raise APIException(
                {'detail': 'Token must be a sended.'}
            )

        try:
            controller = Controller.objects.get(
                token=token
            )
            zone = Zone.objects.create(
                name=validated_data.get('name'),
                zip=validated_data.get('zip'),
                latitude=validated_data.get('latitude'),
                longitude=validated_data.get('longitude'),
                controller=controller
            )
        except Controller.DoesNotExist as exception:
            raise APIException(
                {'error': 'This token does not match with any controller.'}
            )

        return zone

class ZonesInformationSerializer(serializers.HyperlinkedModelSerializer):
    soil_temperature = serializers.FloatField(default=0.0)
    air_temperature = serializers.FloatField(default=0.0)
    precipitation = serializers.FloatField(default=0.0)
    ground_humidity = serializers.FloatField(default=0.0)
    status_modules = serializers.ListField()

    class Meta:
        model = Zone
        fields = (
            'name',
            'zip',
            'latitude',
            'longitude',
            'is_active',
            'controller',
            'soil_temperature',
            'air_temperature',
            'precipitation',
            'ground_humidity',
            'status_modules'
        )
