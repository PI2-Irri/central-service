from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import Module


class ModuleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Module
        fields = (
            'id',
            'rf_address',
            'url'
        )

    def create(self, validated_data):
        rf_address = validated_data.get('rf_address')
        controller = validated_data.get('controller')
        
        try:
            module = Module.objects.get(
                rf_address=rf_address,
                controller=controller
            )
        except Module.DoesNotExist:
            module = Module.objects.create(
                rf_address=rf_address,
                controller=controller
            )

            for measurement in measurements:
                ModuleMeasurements.objects.create(
                    temperature=measurement['temperature'],
                    ground_humidity=measurement['ground_humidity'],
                    battery_level=measurement['battery_level'],
                    is_active=measurement['is_active'],
                    module=module 
                )

        return module