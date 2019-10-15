from rest_framework import serializers
from .models import Controller
from .exceptions import ControllerTokenException
from rest_framework.exceptions import APIException
from .utils import ControllerCommunication
from modules.models import Module

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

        controller = Controller(
            name=validated_data.get('name'),
            is_valid=validated_data.get('is_valid'),
            token=validated_data.get('token'),
            ip_address=validated_data.get('ip_address')
        )

        controller.save()
        controller.owner.add(validated_data.get('owner'))

        modules = ControllerCommunication.get_controller_modules(
            token, 'http://' + ip + controller.port
        )

        for module in modules:
            Module.objects.create(
                rf_address=module["rf_address"],
                controller=controller
            )

        return controller
