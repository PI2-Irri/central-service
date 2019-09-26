from django.conf.urls import url
from django.urls import path
from django.urls import include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from users import urls as users_routers

router = DefaultRouter()

defaultpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', include(router.urls)),
]

urlpatterns = []

# Admin page and main urls
urlpatterns += defaultpatterns

# Login and register path's
urlpatterns += users_routers.urlpatterns
