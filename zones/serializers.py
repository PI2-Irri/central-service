from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
from .models import Controller
from .models import Zone
import pgeocode as pg
import math
import os
import requests


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
        except Exception as e:
            raise APIException(
                {'error': 'Unvalid zipcode'}
            )

        latitude = 0.0
        longitude = 0.0

        if math.isnan(data['latitude']) == False:
            latitude = data['latitude']
        if math.isnan(data['longitude']) == False:
            longitude = data['longitude']

        request = self._kwargs.get('context')['request']

        try:
            controller = Controller.objects.get(
                token=token
            )

            zone = controller.zone_set.filter(name=validated_data.get('name'))

            if zone:
                raise APIException(
                    {'error': 'Zone already registered'}
                )

            try:
                request = requests.post(os.getenv('WEATHER_URL') + '/locations/',
                            data={'location_name':  data['place_name'], 'latitude': latitude, 'longitude': longitude})
            except Exception:
                raise APIException(
                    {'error': 'Could not register'}
                )


            zone = Zone.objects.create(
                name=validated_data.get('name'),
                zip=zipcode,
                controller=controller,
                latitude=latitude,
                longitude=longitude
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

class ActiveZoneSerializer(serializers.HyperlinkedModelSerializer):
    model = Zone
    fields = (
        'status',
        'name',
        'token'
    )
