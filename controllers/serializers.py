from rest_framework import serializers
from .models import Controller
from .models import ControllerSpecification
from .exceptions import ControllerTokenException
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
from modules.models import Module
from modules.serializers import ModuleSerializer
import os


class ControllerSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Controller
        fields = (
            'name',
            'is_active',
            'read',
            'timer',
            'status',
            'token',
            'owner',
            'url'
        )

    def to_internal_value(self, data):
        controller = None

        try:
            controller = Controller.objects.get(token__in=[data.get('token')])
            request = self._kwargs.get('context')['request']
        except Exception:
            return data

        if controller and request.method == 'POST':
            if request.user not in controller.owner.all():
                controller.owner.add(request.user)

                ControllerSpecification.objects.create(
                    owner=request.user,
                    controller=controller,
                    name=data.get('name')
                )

                return data
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

        if token:
            try:
                controller = Controller.objects.get(
                    token=validated_data.get('token')
                )
            except Controller.DoesNotExist:
                if validated_data.get('is_active'):
                    controller = Controller.objects.create(
                        name=validated_data.get('name'),
                        is_active=validated_data.get('is_active'),
                        token=token
                    )
                else:
                    controller = Controller.objects.create(
                        name=validated_data.get('name'),
                        token=token
                    )

                self.to_internal_value(validated_data)

        return controller

    def update(self, instance, validated_data):
        if validated_data.get('name'):
            controller = ControllerSpecification.objects.get(
                name=instance.__dict__['name']
            )
            controller.save(update_fields={'name': validated_data.get('name')})

        # Updates the status and timer fields,
        # if any of them is changed them read=false
        fields = ['status', 'timer']
        for field in fields:
            if not validated_data.get(field):
                continue
            exec('instance.%s = validated_data.get(field)' % (field))
            instance.read = False

        # Updates the read field of the controller
        read = validated_data.get('read')
        if read:
            instance.read = read

        instance.save()

        return instance


class ControllerItemInfoSerializer(serializers.HyperlinkedModelSerializer):
    controller = serializers.CharField()
    zones = serializers.ListField()
    reservoir_level = serializers.FloatField()
    token = serializers.CharField()

    class Meta:
        model = Controller
        fields = (
            'controller',
            'zones',
            'reservoir_level',
            'token'
        )


class ControllerCustomRegistration(serializers.HyperlinkedModelSerializer):
    validation_key = serializers.CharField()

    class Meta:
        model = Controller
        fields = (
            'name',
            'is_active',
            'validation_key',
            'token'
        )

    def to_internal_value(self, data):
        if data.get('validation_key') == os.getenv('SECRET_KEY'):
            return data
        else:
            exception = APIException(
                {'error': 'Validation key not match with registration key.'}
            )
            exception.status_code = 403

            raise exception

    def create(self, validated_data):
        controller = Controller.objects.create(
            name=validated_data.get('name'),
            is_active=True,
            token=validated_data.get('token')
        )

        return controller
