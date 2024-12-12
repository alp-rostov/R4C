from django.urls import path
from .views import *


urlpatterns = [
    path('addrobot', CreateRobot.as_view(), name='addrobot'),
    path('report', create_report_excel, name='report'),
]