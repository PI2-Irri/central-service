from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from rest_framework import permissions
from .models import Zone
from .models import Controller
from .serializers import ZoneSerializer
from .serializers import ZonesInformationSerializer
from .serializers import ActiveZoneSerializer
from rest_framework.exceptions import APIException
from operator import mul
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.none()
    serializer_class = ZoneSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        self.queryset = user.controller_set.all()

        return self.queryset


class ZonesInformationViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.none()
    serializer_class = ZonesInformationSerializer
    permission_classes = (permissions.AllowAny,)
    # authentication_classes = (TokenAuthentication,)

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
                name=zone_name,
            )
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

        if measurement:
            data['soil_temperature'] = 0
            data['air_temperature'] = measurement.air_temperature
            data['precipitation'] = measurement.precipitation
            data['ground_humidity'] = 0
            data['status_modules'] = []

            water_consumption = (
                zone.actuatorsmeasurement_set.filter(controller=controller)
            )

            if water_consumption:
                data['water_consumption'] = water_consumption.last().water_consumption
            else:
                data['water_consumption'] = 0

            valid_modules = 0

            for module in modules:
                if zone.modulesmeasurement_set.filter(module=module).last():
                    data['soil_temperature'] += \
                        zone.modulesmeasurement_set.filter(module=module).last().temperature
                    data['ground_humidity'] += \
                        zone.modulesmeasurement_set.filter(module=module).last().ground_humidity
                    data['status_modules'].append(
                        zone.modulesmeasurement_set.filter(module=module).last().battery_level
                    )
                    valid_modules += 1

            if valid_modules:
                data['soil_temperature'] /= valid_modules
                data['ground_humidity'] /= valid_modules
        else:
            data['soil_temperature'] = 0.0
            data['air_temperature'] = 0.0
            data['precipitation'] = 0
            data['ground_humidity'] = 0.0
            data['status_modules'] = []
            data['water_consumption'] = 0.0

            for module in modules:
                if zone.modulesmeasurement_set.filter(module=module).last():
                    data['status_modules'].append(0)

        return [data]

    @api_view(['POST'])
    def active_zone(request):
        serializer_class = ActiveZoneSerializer(data=request.data)

        if serializer_class.is_valid():
            controller = Controller.objects.get(token=request.data['token'])
            zones = controller.zone_set.filter(is_active=True)

            for zone in zones:
                zone.is_active = False
                zone.save()

            zone = Zone.objects.get(name=request.data['zone_name'])
            zone.is_active = True
            zone.save()

            controller.read = False

            if request.data['status'] == True:
                controller.status = True
                controller.save()

            return Response(
                {'detail': 'Zone activated.'},
                status=HTTP_200_OK
            )
        else:
            raise APIException(
                {'error': 'Invalid fields'}
            )
