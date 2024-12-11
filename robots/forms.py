from django.contrib.auth.forms import UserCreationForm
from django import forms

from robots.models import Robot


class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = '__all__'

