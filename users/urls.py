from .views import CustomUserViewSet
from django.urls import path

app_name = 'users'

urlpatterns = [
    path(r'login/', CustomUserViewSet.login),
    path(r'signup/', CustomUserViewSet.signup)
]
