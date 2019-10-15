from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from .models import Module
from controllers.models import Controller
from .serializers import ModuleSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.none()
    model = Module
    serializer_class = ModuleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user

        controllers = Controller.objects.filter(
            owner=user
        )

        modules = self.model.objects.filter(
            controller__in=controllers
        )

        return modules
