from django.conf.urls import url
from django.urls import path
from django.urls import include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from users import views as users_views

router = DefaultRouter()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', users_views.CustomUserViewSet.login),
    path('signup/', users_views.CustomUserViewSet.signup)
]
