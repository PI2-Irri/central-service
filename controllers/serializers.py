from rest_framework import serializers
from .models import Controller
from .exceptions import ControllerTokenException
from rest_framework.exceptions import APIException
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
            'is_valid',
            'token',
            'owner',
            'ip_address',
            'url'
        )

    def create(self, validated_data):
        ip = validated_data.get('ip_address')
        token = validated_data.get('token')
        # try:
        #     ControllerCommunication.check_token(token, ip)
        # except ControllerTokenException:
        #     raise APIException({"error": "Token does not match with ip token"})

        try:
            controller = Controller(
                name=validated_data.get('name'),
                is_valid=validated_data.get('is_valid'),
                token=token,
                ip_address=ip
            )
            controller.save()
        except Exception:
            controller = Controller.objects.get(
                name=validated_data.get('name'),
                is_valid=validated_data.get('is_valid'),
                token=token,
                ip_address=ip
            )

        controller.owner.add(validated_data.get('owner'))

        modules = ControllerCommunication.get_controller_modules(
            token, 'http://' + ip + controller.port
        )

        for module in modules:
            module_serializer = ModuleSerializer(
                data={
                    'rf_address': module['rf_address']
                }
            )
            if module_serializer.is_valid():
                module_serializer.save(controller=controller)

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
