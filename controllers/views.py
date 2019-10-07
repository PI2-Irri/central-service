from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework.authentication import TokenAuthentication
from .models import Controller
from .models import CustomUser
from .serializers import ControllerSerializer


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
