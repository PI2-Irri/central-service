from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import Module
from controllers.utils import ControllerCommunication
from measurements.models import ModulesMeasurement
from rest_framework.exceptions import APIException


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
        token = validated_data.get('token')

        try:
            controller = Controller.objects.get(
                token=token
            )
            module = Module.objects.get(
                rf_address=rf_address,
                controller=controller
            )
        except Module.DoesNotExist:
            module = Module.objects.create(
                rf_address=rf_address,
                controller=controller
            )
        except Controller.DoesNotExist:
            raise APIException(
                {'detail': 'Token not match with any controller.'}
            )

        return module
