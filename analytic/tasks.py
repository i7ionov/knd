# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.task import periodic_task
from datetime import timedelta

from analytic.general_report import iterate_inspections
from analytic.models import GeneralReport
from iggndb.celery import app
import xlrd, openpyxl
from datetime import datetime
from dictionaries.models import Address, House
from celery.utils.log import get_task_logger
from django.db.models import fields
from django.db.models import Q
from django.http import HttpResponse
import simplejson as json
from django.apps import apps
from iggn_tools import filter, excel
from inspections.models import Inspection


@app.task
def generate_general_report_period(user_id, date_begin, date_end, control_kind_id=None, department_id=None):
    report = GeneralReport(report_status='Формируется...', user_id=user_id, date=datetime.now(), date_begin=date_begin,
                           date_end=date_end)
    inspections = Inspection.objects.filter(act_date__range=(date_begin, date_end))
    # исключаем тестовые проверки
    inspections = inspections.exclude(inspection_result_id=12).exclude(control_form__id=4).exclude(
        control_form__id=5)
    if control_kind_id:
        inspections = inspections.filter(control_kind_id=control_kind_id)
        report.control_kind_id = control_kind_id
    if department_id:
        inspections = inspections.filter(inspector__department_id=department_id)
        report.department_id = department_id
    iterate_inspections(inspections, report)
    return report


@app.task
def generate_general_report_month(month, year):
    pass


@app.task
def export_to_excel(request_post, app_str, model_str, user_id, get_count=False):
    """
    Формирует запрос по указанной модели и применяет к нему фильтрацию.
    От get_count зависит будет ли возвращено количество
    :param request_post: Пример: {'disposal': {'houses': {'contains': ['1;1']}, 'doc_number': {'exact': ['1']}}}
    :param app_str: имя приложения
    :param model_str: имя модели
    :param user_id: id пользователя
    :param get_count: boolean параметр, при true метод возвратит только количество строк, удовлетворяющих условиям фильрации
    при false или отсутствии параметра будет поставлена задача в celery на импорт результата запроса в excel
    :return: HttpResponse типа json с параметром count если get_count равен true
    """
    model = apps.get_model(app_str, model_str)
    q = model.objects.all()
    # по request_post из примера будет две итераци по добавлению фильтра
    # key = 'houses'
    # key = 'doc_number'
    if model_str in request_post:
        for key in request_post[model_str].keys():
            q = filter.add_filter(key, model, q, request_post)
    if get_count:
        return HttpResponse(json.dumps([{'count': str(q.count())}]), content_type='application/json')
    else:
        excel.export_excel(q, user_id)
