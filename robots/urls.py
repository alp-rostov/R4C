from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *


urlpatterns = [
    path('addrobot', CreateRobot.as_view(), name='addrobot'),
]