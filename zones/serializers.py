from rest_framework import serializers
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
            'url'
        )
