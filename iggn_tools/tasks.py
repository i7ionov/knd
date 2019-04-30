# Create your tasks here
from __future__ import absolute_import, unicode_literals

import simplejson as json
from django.apps import apps
from django.http import HttpResponse

from iggn_tools import filter, excel
from iggn_tools.filter import get_filtered_query_set
from iggndb.celery import app
from iggn_tools.excel import export_excel


@app.task
def export_to_excel(request_post, app_str, model_str, user_id, get_count=False):
    """
    Формирует запрос по указанной модели и применяет к нему фильтрацию.
    От get_count зависит будет ли возвращено количество
    :param request_post: Пример: {'filter': {'inspection': {'houses': {'contains': ['1;1']}, 'doc_number': {'exact': ['1']}}},
    'count': {'document': {'doc_type': {'exact': ['проверка']}}},
    'fields_to_count': ['document', 'house']}
    :param app_str: имя приложения
    :param model_str: имя модели
    :param user_id: id пользователя
    :param get_count: boolean параметр, при true метод возвратит только количество строк, удовлетворяющих условиям фильрации
    при false или отсутствии параметра будет поставлена задача в celery на импорт результата запроса в excel
    :return: HttpResponse типа json с параметром count если get_count равен true
    """
    model = apps.get_model(app_str, model_str)
    q = model.objects.all()
    if 'filter' in request_post and model_str in request_post['filter']:
        for key in request_post['filter'][model_str].keys():
            q = filter.add_filter(key, model, q, request_post['filter'])
    if get_count:
        return HttpResponse(json.dumps([{'count': str(q.count())}]), content_type='application/json')
    else:
        excel.export_excel(q, user_id, request_post)


@app.task
def export_to_excel_from_easyui(request, app_str, model_str, user_id, get_count=False):
    model = apps.get_model(app_str, model_str)
    q = get_filtered_query_set(model, request)
    excel.export_excel(q, user_id, request)
