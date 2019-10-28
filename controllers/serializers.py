from rest_framework import serializers
from .models import Controller
from .exceptions import ControllerTokenException
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
from .utils import ControllerCommunication
from modules.models import Module
from modules.serializers import ModuleSerializer


class ControllerSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Controller
        fields = (
            'id',
            'name',
            'is_active',
            'token',
            'owner',
            'url'
        )

    def to_internal_value(self, data):
        controller = None

        try:
            controller = Controller.objects.get(token=data.get('token'))
            user = self._kwargs.get('context')['request'].user
        except Exception:
            return data

        if controller:
            if user not in controller.owner.all():
                controller.owner.add(user)
                succefull_association = APIException(
                    {'detail': 'The user was associated with this controller.'}
                )
                succefull_association.status_code = 200

                raise succefull_association
            else:
                invalid_association = APIException(
                    {
                        'detail': ('This user has already been associated '
                                   'with this controller.')
                    }
                )
                invalid_association.status_code = 400

                raise invalid_association
        else:
            return data

    def create(self, validated_data):
        token = validated_data.get('token')

        try:
            controller = Controller(
                name=validated_data.get('name'),
                is_active=validated_data.get('is_active'),
                token=token
            )
            controller.save()
            controller.owner.add(validated_data.get('owner'))
        except Exception:
            controller = Controller.objects.get(
                name=validated_data.get('name'),
                is_active=validated_data.get('is_active'),
                token=token
            )


        return controller


class ControllerItemInfoSerializer(serializers.HyperlinkedModelSerializer):
    controller = serializers.CharField()
    zones = serializers.ListField()
    reservoir_level = serializers.FloatField()

    class Meta:
        model = Controller
        fields = (
            'controller',
            'zones',
            'reservoir_level'
        )
