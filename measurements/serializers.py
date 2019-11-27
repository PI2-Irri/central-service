from rest_framework import serializers
from .models import ActuatorsMeasurement
from .models import ModulesMeasurement
from .models import ZoneMeasurement
from .models import Zone
from .models import Controller
from modules.models import Module
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist


class ActuatorsMeasurementSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ActuatorsMeasurement
        fields = (
            'id',
            'water_consumption',
            'reservoir_level',
            'url'
        )

    def to_internal_value(self, data):
        if data.get('token'):
            return data
        else:
            raise APIException(
                {'detail': 'Token is required.'}
            )

    def create(self, validated_data):
        controller = None

        try:
            controller = Controller.objects.get(
                token=validated_data.get('token')
            )
            zone = controller.zone_set.get(
                is_active=True
            )
        except Controller.DoesNotExist:
            raise APIException(
                {'error': 'Token does not match with any controller.'}
            )
        except Zone.DoesNotExist:
            raise APIException(
                {'error': 'Zone not found'}
            )

        measurement = ActuatorsMeasurement.objects.create(
            water_consumption=int(validated_data.get('water_consumption')),
            reservoir_level=int(validated_data.get('reservoir_level')),
            controller=controller,
            zone=zone
        )

        return measurement


class ModulesMeasurementSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ModulesMeasurement
        fields = (
            'temperature',
            'ground_humidity',
            'battery_level',
            'module'
        )

    def to_internal_value(self, data):
        if data.get('token'):
            if data.get('rf_address'):
                return data
            else:
                raise APIException(
                    {'detail': 'RF Address is required.'}
                )
        else:
            raise APIException(
                {'detail': 'Token is required.'}
            )

    def create(self, validated_data):
        controller = None
        module = None


        try:
            controller = Controller.objects.get(
                token=validated_data.get('token')
            )
            module = controller.module_set.get(
                rf_address=validated_data.get('rf_address')
            )
            zone = controller.zone_set.get(
                is_active=True
            )
        except Controller.DoesNotExist:
            raise APIException(
                {'error': 'Token does not match with any controller.'}
            )
        except Module.DoesNotExist:
            module = Module.objects.create(
                rf_address=validated_data.get('rf_address'),
                controller=controller
            )
        except Zone.DoesNotExist:
            raise APIException(
                {'error': 'Zone not found'}
            )
            
        measurement = ModulesMeasurement.objects.create(
            temperature=float(validated_data.get('soil_temperature')),
            ground_humidity=int(validated_data.get('ground_humidity')),
            battery_level=int(validated_data.get('battery_level')),
            module=module,
            zone=zone
        )

        return measurement


class ZoneMeasurementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ZoneMeasurement
        fields = (
            'air_temperature',
            'precipitation'
        )
