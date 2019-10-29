from django.conf.urls import url
from django.urls import path
from django.urls import include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from controllers.views import ControllerViewSet
from controllers.views import ControllerItemInfoViewSet
from controllers import views as controller_views
from zones import views as zone_views
from measurements import views as measurements_views
from modules import views as modules_views

from users.views import CustomUserViewSet

router = DefaultRouter()

router.register(
    r'controllers_info',
    ControllerItemInfoViewSet,
    basename='controllers_info'
)
router.register(r'controllers', ControllerViewSet)
router.register(r'zones', zone_views.ZoneViewSet)
router.register(
    r'modules',
    modules_views.ModuleViewSet
)
router.register(
    r'actuators_measurements',
    measurements_views.ActuatorsMeasurementViewSet
)
router.register(
    r'modules_measurements',
    measurements_views.ModulesMeasurementViewSet
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', include(router.urls)),
    path(r'login/', CustomUserViewSet.login),
    path(r'signup/', CustomUserViewSet.signup)
]
