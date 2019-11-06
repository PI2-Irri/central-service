from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
from .models import Controller
from .models import Zone

import pgeocode as pg



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
            nomi = pg.Nominatim('br')
            zipcode = validated_data.get('zip')[0:3] + '00-000'
            data = nomi.query_postal_code(zipcode)
        except:
            raise APIException(
                {'error': 'Unvalid zipcode'}
            )

        request = self._kwargs.get('context')['request']

        try:
            controller = Controller.objects.get(
                token=token
            )

            zone = controller.zone_set.filter(validated_data.get('name'))

            if zone:
                raise APIException(
                {'error': 'Zone already registered'}
            ) 

            zone = Zone.objects.create(
                name=validated_data.get('name'),
                zip=zipcode,
                controller=controller,
                latitude=data['latitude'],
                longitude=data['longitude']
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
