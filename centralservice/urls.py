from django.conf.urls import url
from django.urls import path
from django.urls import include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from controllers import views as controller_views
from zones import views as zone_views
from measurements import views as measurements_views

from users import urls as users_routers

router = DefaultRouter()

router.register(r'controllers', controller_views.ControllerViewSet)
router.register(r'zones', zone_views.ZoneViewSet)
router.register(
    r'actuators_measurements',
    measurements_views.ActuatorsMeasurementViewSet
)

defaultpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', include(router.urls)),
]

urlpatterns = []

# Admin page and main urls
urlpatterns += defaultpatterns

# Login and register path's
urlpatterns += users_routers.urlpatterns
