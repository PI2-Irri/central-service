from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import Module
from controllers.utils import ControllerCommunication
from measurements.models import ModulesMeasurement


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

            measurements = ControllerCommunication.collect_from_controller(
                'http://' + \
                controller.ip_address + \
                controller.port + \
                'module_measurements/' + \
                '?rf_address={}'.format(rf_address)
            )

            for measurement in measurements:
                ModulesMeasurement.objects.create(
                    temperature=measurement['temperature'],
                    ground_humidity=measurement['ground_humidity'],
                    battery_level=measurement['battery_level'],
                    module=module
                )

        return module
