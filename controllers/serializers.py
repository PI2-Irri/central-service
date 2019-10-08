from rest_framework import serializers
from .models import Controller


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
            'url'
        )

    def create(self, validated_data):
        controller = Controller(
            name=validated_data.get('name'),
            is_valid=validated_data.get('is_valid'),
            token=validated_data.get('token')
        )

        controller.save()
        controller.owner.add(validated_data.get('owner'))

        return controller
