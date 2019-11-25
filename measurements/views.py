from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework.authentication import TokenAuthentication
from .models import ActuatorsMeasurement
from .models import ModulesMeasurement
from .models import ZoneMeasurement
from controllers.models import Controller
from .serializers import ActuatorsMeasurementSerializer
from .serializers import ModulesMeasurementSerializer
from .serializers import ZoneMeasurementSerializer


class ActuatorsMeasurementViewSet(viewsets.ModelViewSet):
    queryset = ActuatorsMeasurement.objects.none()
    model = ActuatorsMeasurement
    serializer_class = ActuatorsMeasurementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        token = self.request.query_params.get('token')

        if token is None:
            raise APIException(
                {'error': 'Token is required.'}
            )

        controller = Controller.objects.get(token=token)

        if controller is None:
            raise APIException(
                {'error': 'Token does not match in database.'}
            )

        self.queryset = self.model.objects.filter(
            controller=controller
        )

        return self.queryset


class ModulesMeasurementViewSet(viewsets.ModelViewSet):
    queryset = ModulesMeasurement.objects.none()
    model = ModulesMeasurement
    serializer_class = ModulesMeasurementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        token = self.request.query_params.get('token')

        if token is None:
            raise APIException(
                {'error': 'Token is required.'}
            )

        controller = Controller.objects.get(token=token)

        if controller is None:
            raise APIException(
                {'error': 'Token does not match in database.'}
            )

        self.queryset = self.model.objects.filter(
            controller=controller
        )

        return self.queryset


class ZoneMeasurementViewSet(viewsets.ModelViewSet):
    queryset = ZoneMeasurement.objects.all()
    model = ZoneMeasurement
    serializer_class = ZoneMeasurementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
