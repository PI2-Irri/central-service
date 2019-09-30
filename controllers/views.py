from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import Controller 
from .serializers import ControllerSerializer


class ControllerViewSet(viewsets.ModelViewSet):
    queryset = Controller.objects.all()
    serializer_class = ControllerSerializer
    permission_classes = (permissions.AllowAny,)
