from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework.authentication import TokenAuthentication
from .models import Controller
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
    queryset = []
    serializer_class = ControllerItemInfoSerializer
    permission_classes = (permissions.AllowAny)

    def get_queryset(self):
        user = self.request.user
        data = {}

        controllers = user.controller_set.all()

        for controller in controllers:
            measurement = controller.actuatormeasurement_set.last()
            data['controller'] = controller
            data['zones'] = controller.zone_set.all()
            data['reservoir_level'] = (
                measurement.reservoir_level
            )
            data['water_consumption'] = (
                measurement.water_consumption
            )

            self.queryset.append(data)

        return self.queryset
