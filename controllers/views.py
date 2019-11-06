from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework.authentication import TokenAuthentication
from .models import Controller
from .models import ControllerSpecification
from .models import CustomUser
from .serializers import ControllerSerializer
from .serializers import ControllerItemInfoSerializer


class ControllerViewSet(viewsets.ModelViewSet):
    queryset = Controller.objects.none()
    serializer_class = ControllerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        self.queryset = user.controller_set.all()

        return self.queryset


class ControllerItemInfoViewSet(viewsets.ModelViewSet):
    queryset = Controller.objects.none()
    serializer_class = ControllerItemInfoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        result = []

        controllers = user.controller_set.all()

        for controller in controllers:
            data = {}
            measurement = controller.actuatorsmeasurement_set.last()

            data['controller'] = ControllerSpecification.objects.get(
                controller=controller
            )
            data['token'] = controller.token
            data['zones'] = (
                [
                    {
                        'name': zone.name,
                        'zip': zone.zip,
                        'latitude': zone.latitude,
                        'longitude': zone.longitude
                    }
                    for zone in controller.zone_set.all()
                ]
            )
            if measurement:
                data['reservoir_level'] = (
                    measurement.reservoir_level
                )
                data['water_consumption'] = (
                    measurement.water_consumption
                )
            else:
                data['reservoir_level'] = 0
                data['water_consumption'] = 0

            result.append(data)

        return result
