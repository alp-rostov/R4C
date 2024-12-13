from django.http import JsonResponse
from django.views.generic import CreateView, TemplateView
from robots.forms import RobotForm


class CreateRobot(TemplateView):
    template_name = 'robot/createrobot.html'

    def post(self, request, *args, **kwargs):
        model = self.request.POST.get('model')
        version = self.request.POST.get('version')
        serial_number = f'{model}-{version}'
        copy_request = self.request.POST.copy()
        copy_request.appendlist('serial',serial_number)
        form = RobotForm(copy_request)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Робот добавлен'})
        else:
            return JsonResponse({'message': 'Ошибка валидации', 'errors':form.errors})