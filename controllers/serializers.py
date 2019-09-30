from rest_framework import serializers
from .models import Controller


class ControllerSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Controller
        fields = (
            'id',
            'name',
            'is_valid',
            'token',
            'url'
        )
