from django.conf.urls import url
from django.urls import path
from django.urls import include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', include(router.urls))
]
