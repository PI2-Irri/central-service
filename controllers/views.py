from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.exceptions import APIException
from .models import Controller
from .models import CustomUser
from .serializers import ControllerSerializer


class ControllerViewSet(viewsets.ModelViewSet):
    queryset = Controller.objects.none()
    serializer_class = ControllerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        username = self.request.query_params.get('username')
        password = self.request.query_params.get('password')
        user = None

        params = {
            'username': username,
            'password': password
        }

        self.validate_query_params(params)

        try:
            user = CustomUser.objects.get(
                username=username
            )
            self.queryset = user.controller_set.all()
        except CustomUser.DoesNotExist:
            raise APIException('Invalid credentials.')

        return self.queryset

    def validate_query_params(self, params):
        pass
