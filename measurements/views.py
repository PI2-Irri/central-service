from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework.authentication import TokenAuthentication
from .models import ActuatorsMeasurement
from controllers.models import Controller
from .serializers import ActuatorsMeasurementSerializer


class ActuatorsMeasurementViewSet(viewsets.ModelViewSet):
    queryset = ActuatorsMeasurement.objects.none()
    model = ActuatorsMeasurement
    serializer_class = ActuatorsMeasurementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        token = self.request.query_params.get('token')

        controller = Controller.objects.get(token=token)

        self.queryset = self.model.objects.filter(
            controller=controller
        )

        return self.queryset
