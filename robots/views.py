from django.db.models import Count
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.generic import CreateView, TemplateView
from robots.forms import RobotForm
from robots.models import Robot
from robots.utils import current_monday, createreportfile


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


def create_report_excel(request, **kwargs):
    queryset = (Robot.objects
                .values('model', 'version')
                .annotate(quantity=Count("model"))
                .filter(created__gte=current_monday()))
    if not queryset:
        return HttpResponse("No robots. The report is empty.")
    createreportfile(queryset, 'analitics.xlsx')
    return FileResponse(open('analitics.xlsx', 'rb'), as_attachment=False, filename= 'analitics.xlsx' )
