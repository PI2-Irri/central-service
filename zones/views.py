from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import Zone
from .serializers import ZoneSerializer


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    permission_classes = (permissions.AllowAny,)
