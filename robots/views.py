from django.db.models import Count
from django.http import JsonResponse
from django.views.generic import CreateView, TemplateView, ListView
from robots.forms import RobotForm
from robots.models import Robot
import pandas as pd

class CreateRobot(TemplateView):
    template_name = 'robot/createrobot.html'
    def post(self, request, *args, **kwargs):
        form = RobotForm(self.request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Робот добавлен'})
        else:
            return JsonResponse({'message': 'Ошибка валидации'})

class ListRobotsReport(ListView):
    model = Robot
    template_name = 'robot/listrobotsreport.html'
    context_object_name = 'robots'

    def get_queryset(self):
        queryset = super().get_queryset().values('model', 'version').annotate(
            quantity=Count("model"))
        c=Robot.objects.all().values('model').distinct()
        data_list=[]
        for i in c:
            d = queryset.filter(model=i['model'])
            models = []
            versions = []
            quantity = []
            for a in d:
                models.append(a['model'])
                versions.append(a['version'])
                quantity.append(a['quantity'])
            data = {'МОДЕЛЬ': models,
                'ВЕРСИЯ': versions,
                'КОЛИЧЕСТВО ЗА НЕДЕЛЮ': quantity}
            data_list.append(data)

        with pd.ExcelWriter('analitics.xlsx', engine="xlsxwriter",
                            mode='w') as excel_writer:
            for i in data_list:
                df = pd.DataFrame(i)
                df.to_excel(excel_writer, sheet_name=i['МОДЕЛЬ'][0], index=False)
        return queryset