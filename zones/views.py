from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from rest_framework import permissions
from .models import Zone
from .models import Controller
from .serializers import ZoneSerializer
from .serializers import ZonesInformationSerializer


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.none()
    serializer_class = ZoneSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        self.queryset = user.controllers_set.all()

        return self.queryset


class ZonesInformationViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.none()
    serializer_class = ZonesInformationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        token = self.request.query_params.get('token')
        user = self.request.user

        try:
            controller = Controller.objects.get(
                token=token
            )
        except Controller.DoesNotExist:
            raise APIException(
                {'error': 'Token not match with any controller.'}
            )

        zones = controller.zones_set.all()
        modules = controller.modules_set.all()
        result = []

        for zone in zones:
            data = {}

            data['name'] = zone.name
            data['zip'] = zone.zip
            data['latitude'] = zone.latitude
            data['longitude'] = zone.longitude
            data['is_active'] = zone.is_active
            data['controller'] = zone.controller

            if zone.is_active:
                data['soil_temperature'] = 33.2
                data['air_temperature'] = 35.7
                data['precipitation'] = 10
                data['ground_humidity'] = 21.0
                data['status_modules'] = (
                    [
                        module.modulesmeasurement_set.last()['battery_level']
                        for module in modules
                    ]
                )
            else:
                data['soil_temperature'] = 0.0
                data['air_temperature'] = 0.0
                data['precipitation'] = 0
                data['ground_humidity'] = 0.0
                data['status_modules'] = [0, 0, 0]

            result.append(data)

        return result
