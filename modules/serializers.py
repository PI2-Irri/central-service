from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import Module
from controllers.utils import ControllerCommunication
from measurements.models import ModulesMeasurement
from rest_framework.exceptions import APIException
from .models import Controller


class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    token = serializers.CharField(read_only=True)

    class Meta:
        model = Module
        fields = (
            'id',
            'token',
            'rf_address',
            'url'
        )

    def to_internal_value(self, data):
        
        if(data.get('token') and data.get('rf_address')):
            return data

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
        except Module.DoesNotExist:
            module = Module.objects.create(
                rf_address=int(rf_address),
                controller=controller
            )

        return module
