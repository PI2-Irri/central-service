from django.conf.urls import url
from django.urls import path
from django.urls import include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from controllers.views import ControllerViewSet
from controllers.views import ControllerItemInfoViewSet
from controllers.views import ControllerCustomRegistrationViewSet
from controllers import views as controller_views
from zones.views import ZoneViewSet
from zones.views import ZonesInformationViewSet
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
router.register(
    r'controller_regs',
    ControllerCustomRegistrationViewSet,
    basename='controller_regs'
)
router.register(r'zones', ZoneViewSet)
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
router.register(
    r'zones_info',
    ZonesInformationViewSet,
    basename='zones_info'
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', include(router.urls)),
    path(r'login/', CustomUserViewSet.login),
    path(r'signup/', CustomUserViewSet.signup)
]
