from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import Module
from controllers.utils import ControllerCommunication
from measurements.models import ModulesMeasurement
from rest_framework.exceptions import APIException
from .models import Controller


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
                rf_address=int(rf_address),
                controller=controller
            )
        except Controller.DoesNotExist:
            raise APIException(
                {'detail': 'Token not match with any controller.'}
            )
        except ValueError:
            raise APIException(
                {'error': 'Field rf_address is not a integer field.'}
            )

        return module
