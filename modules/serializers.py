from rest_framework import serializers
from .models import Module


class ModuleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Module
        fields = (
            'id',
            'rf_address',
            'battery_level',
            'url'
        )
