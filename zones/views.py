from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from rest_framework import permissions
from .models import Zone
from .models import Controller
from .serializers import ZoneSerializer
from .serializers import ZonesInformationSerializer
from rest_framework.exceptions import APIException
from operator import mul
from rest_framework.decorators import action


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.none()
    serializer_class = ZoneSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        print(100*"*")
        user = self.request.user
        print(100*"*")
        self.queryset = user.controllers_set.all()

        return self.queryset


class ZonesInformationViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.none()
    serializer_class = ZonesInformationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        token = self.request.query_params.get('token')
        zone_name = self.request.query_params.get('zone_name')

        user = self.request.user

        try:
            controller = Controller.objects.get(
                token=token
            )
        except Controller.DoesNotExist:
            raise APIException(
                {'error': 'Token not match with any controller.'}
            )

        try:
            zone = controller.zone_set.get(
                name=zone_name
            )
            print(zone)
        except Zone.DoesNotExist:
            raise APIException({'detail': 'There is no zone associated with this user'})

        modules = controller.module_set.all()

        data = {}

        data['name'] = zone.name
        data['zip'] = zone.zip
        data['latitude'] = zone.latitude
        data['longitude'] = zone.longitude
        data['is_active'] = zone.is_active
        data['controller'] = zone.controller

        measurement = zone.zonemeasurement_set.last()

        if zone.is_active and measurement:
            data['soil_temperature'] = 0
            data['air_temperature'] = measurement.air_temperature
            data['precipitation'] = measurement.precipitation
            data['ground_humidity'] = 0
            data['status_modules'] = []
            valid_modules = 0

            for module in modules:
                if module.modulesmeasurement_set.last():
                    data['soil_temperature'] += \
                        module.modulesmeasurement_set.last()['temperature']
                    data['ground_humidity'] += \
                        module.modulesmeasurement_set.last()['ground_humidity']
                    data['status_modules'].append(
                        module.modulesmeasurement_set.last()['battery_level']
                    )
                    valid_modules += 1

            data['soil_temperatures'] /= valid_modules
            data['ground_humidity'] /= valid_modules
        else:
            data['soil_temperature'] = 0.0
            data['air_temperature'] = 0.0
            data['precipitation'] = 0
            data['ground_humidity'] = 0.0
            data['status_modules'] = []

            for module in modules:
                if module.modulesmeasurement_set.last():
                    data['status_modules'].append(0)

        return [data]

    @action(detail=True, methods=['post'])
    def active_zone(self, request):
        serializer_class = ActiveZoneSerializer(data=request.data)

        if serializer_class.is_valid():
            zones = Zone.objects.filter(is_active=True)

            for zone in zones:
                zone.is_active = False
                zone.save()

            zone = Zone.objects.get(name=request.data['name'])
            zone.is_active = True
            zone.save()

            if request.data['status'] == True:
                controller = Controller.objects.get(token=request.data['token'])
                controller.status = True
                controller.save()
        else:
            raise APIException(
                {'error': 'Invalid fields'}
            )
