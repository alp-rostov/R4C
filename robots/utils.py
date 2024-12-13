import pandas as pd
from django.core.mail import EmailMultiAlternatives
from django.db.models import QuerySet
from datetime import timedelta, date

from django.template.loader import render_to_string


def createreportfile(queryset:QuerySet, filename:str) -> None:
    """ create excel file """
    c = queryset.values('model').distinct()
    data_list = []
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

    with pd.ExcelWriter(filename, engine="xlsxwriter",
                        mode='w') as excel_writer:
        for i in data_list:
            df = pd.DataFrame(i)
            df.to_excel(excel_writer, sheet_name=i['МОДЕЛЬ'][0], index=False)

def send_email(email:str='', subject_:str=f'Уведомление о наличии робота', template_name_:str = 'robot/email.html', context_:dict={}):
    """send email"""
    html_content = render_to_string(
        template_name=template_name_,
        context=context_
    )
    msg = EmailMultiAlternatives(
        subject=subject_,
        from_email='admin@sakhlis-remonti.ge',
        to=[email],
        )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def current_monday() -> date:
    """ Monday date of this week """
    now = date.today()
    current_weekday = now.weekday()
    current_monday = date.today() - timedelta(days=current_weekday)
    return current_monday