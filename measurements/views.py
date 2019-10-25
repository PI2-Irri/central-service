from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework.authentication import TokenAuthentication
from .models import ActuatorsMeasurement
from .models import ModulesMeasurement
from controllers.models import Controller
from .serializers import ActuatorsMeasurementSerializer
from .serializers import ModulesMeasurementSerializer


class ActuatorsMeasurementViewSet(mixins.RetrieveModelMixin,
                                  mixins.DestroyModelMixin,
                                  mixins.ListModelMixin,
                                  viewsets.GenericViewSet):
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


class ModulesMeasurementViewSet(mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
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
