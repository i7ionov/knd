"""Модуль содержит методы для формирования QuerySet'ов"""

import simplejson as json
from datetime import datetime
from django.db.models import fields
from django.db.models import Q
from django.db import models
from django.http import HttpResponse

from dictionaries.models import Address, House, Document
from iggn_tools.tools import get_value, datetime_handler


def filtered_table_json_response(request, model, func=None, filtering_rules=None):
    """Метод создает типовой JSON ответ на request, генерируемый EasyUI DataGrid.
    Response содержит отфильтрованую по критериям таблицу указанной модели.
    :param func: функция добавляющая дополнительные поля для выдачи
    :param filtering_rules: дополнительные правила фильтрафии
    """
    objects = []
    # получаем отфильтрованый QuerySet
    query = get_filtered_query_set(model, request.POST, filtering_rules).distinct()
    print(query)
    count = query.count()
    # пагинация
    if "rows" in request.POST:
        page = 1
        rows = int(request.POST['rows'])
        if "page" in request.POST:
            page = int(request.POST['page'])
        start = rows * (page - 1)
        end = start + rows
        query = query[start:end]
    # получаем список полей модели для отображения
    fields = get_model_columns([], model)
    for item in query:
        object = {'id': item.pk}
        for field in fields:
            object[field['prefix'].replace('.', '__') + field['name']] = get_value(item, field['prefix'] + field[
                'name'])
        if func:
            object = func(object, item)
        objects.append(object)
    data = {"total": count, "rows": objects}
    return HttpResponse(json.dumps(data, default=datetime_handler), content_type='application/json')


def get_filtered_query_set(model, request_post, filtering_rules=None):
    """
    Метод создает QuerySet по указанной модели, применяет к ней фильтрации, сортировки по переданным правилам
    :param model: Модель, по которой создается QuerySet
    :param request: POST request, полученный от EasyUI DataGrid
    :param filtering_rules: дополнительные правила фильтрафии
    :return: QuerySet
    """
    # фильтрация
    if 'filterRules' in request_post:
        # [{"field":"name","op":"contains","value":"org"}]
        rules = json.loads(request_post['filterRules'])
    else:
        rules = []
    if filtering_rules:
        pass
    if filtering_rules:
        rules.extend(filtering_rules)
    # сортировка
    if "sort" in request_post:
        sort = request_post['sort']
        order = request_post['order']
        if order == 'desc':
            sort = '-' + sort
    else:
        sort = 'pk'
    query = filter_query(model, rules).order_by(sort)
    return query


def filter_query(model, rules):
    """
    Метод создает QuerySet по указанной модели, применяет к ней фильтрации по всем переданным правилам
    :param model: Модель, по которой создается QuerySet
    :param rules: Список правил для фильтрации в виде объекта, экспортированного из JSON.
    Пример: [{"nested_object__field":"name","op":"contains","value":"org"}],

    Поле op может содержать следующие значения: contains, less, greater
    :return: QuerySet с добавленной фильтрацией
    """
    query = model.objects.all()
    if rules:
        for rule in rules:
            query = add_filter_from_easyui(query, rule)
    return query


def add_filter_from_easyui(query, rule):
    """
    Метод добавляет фильтрацию к переданному QuerySet по заданному правилу
    :param query: QuerySet
    :param rule: Правило для фильтрации в виде объекта, экспортированного из JSON.
    Пример: [{"field":"name","op":"contains","value":"org"}].
    Поле op может содержать следующие значения: contains, less, greater
    :return: QuerySet с добавленной фильтрацией
    """

    field = str(rule['field']).replace('.', '__')
    criteria = rule['value']
    if criteria == '' or criteria is None:
        return query
    if rule['op'] == 'between':
        try:
            date_begin = datetime.strptime(criteria.split('-')[0], '%d.%m.%Y')
        except (ValueError, KeyError):
            date_begin = datetime.strptime('01.01.2015', '%d.%m.%Y')
        try:
            date_end = datetime.strptime(criteria.split('-')[1], '%d.%m.%Y')
        except (ValueError, KeyError):
            date_end = datetime.now()
        criteria = (date_begin, date_end)
        field = field + '__range'
    elif rule['op'] == 'contains':
        field = field + '__icontains'
    elif rule['op'] == 'less':
        field = field + '__lt'
    elif rule['op'] == 'greater':
        field = field + '__gt'
    elif rule['op'] == 'isnone':
        if criteria == '1':
            field = field
            criteria = None
        else:
            field = field + '_id__gt'
            criteria = 0
    query = query.filter(Q(**{field: criteria}))
    return query


def get_model_columns(field_list, model, prefix='', parent_verbose_name=''):
    """
    Метод создает список полей у которых было заполненно verbose_name, работает рекурсивно.
    :param field_list: Объект с полями: verbose_name, name, prefix, field
    :param model: Модель, поля которой нужно получить
    :param prefix: Префикс для поля. Используется в итерациях рекурсии. Хранит имя родительского поля
    :param parent_verbose_name: Используется в итерациях рекурсии. Хранит человекочитаемое название
    родительского поля
    :return: Возвращает список объектов с полями:
    verbose_name - человекочитаемое название поля,
    name - имя поля,
    prefix - имя родительского поля с точкой на конце,
    field - ссылка на сам объект поля
    """
    # выберем поля с verbose_name
    for col, field in enumerate(model._meta.get_fields()):
        field_verbose_name = ''
        if hasattr(field, 'verbose_name') and field.verbose_name:
            try:
                if field.__class__ == fields.AutoField or \
                        field.__class__ == models.OneToOneField:
                    continue
                if field.__class__ == fields.related.ForeignKey or \
                        field.__class__ == fields.related.ManyToManyRel:
                    field_list = get_model_columns(field_list, field.related_model, prefix + field.name + '.',
                                                   field.verbose_name)
                else:
                    if field.name == 'text':
                        field_verbose_name = parent_verbose_name
                    else:
                        field_verbose_name = field.verbose_name
                    field_list.append(
                        {'verbose_name': field_verbose_name, 'name': field.name, 'prefix': prefix, 'field': field})
            except AttributeError:
                pass
    return field_list


def get_model_foreign_fields(model):
    result = []
    for field in model._meta._get_fields():
        if field.__class__ == models.fields.reverse_related.ManyToOneRel or field.__class__ == fields.related.ManyToManyField or field.__class__ == fields.reverse_related.ManyToManyRel:
            if hasattr(field, 'attname'):
                related_name = field.attname
            elif hasattr(field, 'related_name') and field.related_name:
                related_name = field.related_name
            else:
                related_name = field.name + '_set'
            result.append({'field': field, 'verbose_name': field.related_model._meta.verbose_name,
                           'app': field.related_model._meta.app_label, 'meta': field.related_model._meta, 'related_name': related_name})
            if field.name == 'children' or field.name == 'document':
                for f in Document.get_one_to_one_rel(Document):
                    result.append({'field': f, 'verbose_name': f.related_model._meta.verbose_name,
                                   'app': f.related_model._meta.app_label, 'meta': f.related_model._meta, 'related_name': related_name})
    return result


def get_field_by_model(object, model):
    """Возвращает имя поля со связью у объекта по модели"""
    for field in get_model_foreign_fields(object._meta.model):
        if field['field'].related_model == model:

            return field['related_name']

    return None


def add_filter(field_str, model, q, request_post, model_name=None):
    """
    :param field_str: имя поля для фильтрации, в формате object__field
    :param model: модель
    :param q: исходный запрос
    :param request_post: Пример: {'disposal': {'houses': {'contains': ['1;1']}, 'doc_number': {'exact': ['1']}}}
    :return:
    """
    field_key = field_str
    if model_name is None:
        model_name = model._meta.model_name
    else:
        field_key = field_key.replace(model_name+'__', '')
    for f in field_str.split('__'):
        fld = model._meta.get_field(f)
        if fld.related_model and fld.__class__ != fields.related.ManyToManyField:
            model = fld.related_model
        field = fld.name
    if model._meta.get_field(field).__class__ == fields.DateField:
        try:
            date_begin = datetime.strptime(request_post[model_name][field_key]['begin'][0], '%d.%m.%Y')
        except (ValueError, KeyError):
            date_begin = datetime.strptime('01.01.2015', '%d.%m.%Y')
        try:
            date_end = datetime.strptime(request_post[model_name][field_key]['end'][0], '%d.%m.%Y')
        except (ValueError, KeyError):
            date_end = datetime.now()
        q = q.filter(Q(**{field_str + '__range': (date_begin, date_end)}))
    elif model._meta.get_field(field).__class__ == fields.CharField \
            or model._meta.get_field(field).__class__ == fields.TextField \
            or model._meta.get_field(field).__class__ == fields.related.ForeignKey:
        mode = list(request_post[model_name][field_key].keys())[0]
        q = q.filter(Q(**{field_str + '__' + mode: request_post[model_name][field_key][mode][0]}))
    elif model._meta.get_field(field).__class__ == fields.IntegerField:
        try:
            begin = int(request_post[model_name][field_key]['begin'][0])
        except (ValueError, KeyError):
            begin = 0
        try:
            end = int(request_post[model_name][field_key]['end'][0])
        except (ValueError, KeyError):
            end = 99
        q = q.filter(Q(**{field_str + '__range': (begin, end)}))
    elif model._meta.get_field(field).__class__ == fields.related.ManyToManyField:
        if field == 'houses':
            for i in request_post[model_name][field_key]['contains']:
                addr = i.split(';')
                try:
                    address = Address.objects.get(id=addr[0])
                    house = House.objects.get(address=address, number=addr[1])
                    q = q.filter(Q(**{field_str: house}))
                except(Address.DoesNotExist, House.DoesNotExist):
                    pass
        else:
            try:
                for i in request_post[model_name][field_key]['contains']:
                    q = q.filter(Q(**{field_str: i}))
            except KeyError:
                print('Error')
    return q
