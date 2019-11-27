from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework.authentication import TokenAuthentication
from .models import Schedule
from controllers.models import Controller
from .serializers import SchedulesFromController
from .serializers import ScheduleSerializer
from .serializers import NotificationSerializer


class SchedulesViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.none()
    serializer_class = ScheduleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)


class SchedulesFromControllerViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.none()
    serializer_class = SchedulesFromController
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        token = self.request.query_params.get('token')

        try:
            controller = Controller.objects.get(
                token=token
            )
        except Controller.DoesNotExist:
            raise APIException(
                {'error': 'Token does not match with any controller.'}
            )

        zones = controller.zone_set.all()
        informations = []

        for zone in zones:
            schedules = zone.schedule_set.all().order_by('schedule')

            dates = []
            dates = list(
                set(
                    [
                        schedule.schedule.strftime('%Y-%m-%d')
                        for schedule in schedules
                    ]
                )
            )

            for date in dates:
                data = {}
                data['zone'] = zone.name
                data['attr'] = {
                    'dates': date,
                    'dot': 'blue'
                }
                data['schedule'] = list(
                    set(
                        schedule.schedule.strftime('%H:%M')
                        for schedule in
                        schedules.filter(
                            schedule__gte=(date + ' 00:00:00'),
                            schedule__lte=(date + ' 23:59:59')
                        )
                    )
                )

                informations.append(data)

        return informations

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.none()
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        self.queryset = user.notification_set.all().reverse()[:10]

        return self.queryset