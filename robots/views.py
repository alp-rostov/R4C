from datetime import datetime
from django.http import JsonResponse
from django.views.generic import CreateView, TemplateView
from robots.forms import RobotForm


class CreateRobot(TemplateView):
    template_name = 'robot/createrobot.html'
    def post(self, request, *args, **kwargs):
        form = RobotForm(self.request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Робот добавлен'})
        else:
            return JsonResponse({'message': 'Ошибка валидации', 'errors':form.errors})