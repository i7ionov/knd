"""Модуль содержит методы для формирования QuerySet'ов"""
import simplejson as json
import django
from datetime import date, datetime
from django.db.models import fields
from django.db.models import Q
from django.db import models
from django.http import HttpResponse


def filtered_table_json_response(request, model, func=None):
    """Метод создает типовой JSON ответ на request, генерируемый EasyUI DataGrid.
    Response содержит отфильтрованую по критериям таблицу указанной модели.
    :param func: функция добавляющая дополнительные поля для выдачи"""
    objects = []
    # пагинация
    page = 1
    rows = 10
    if "page" in request.POST:
        page = int(request.POST['page'])
    if "rows" in request.POST:
        rows = int(request.POST['rows'])
    start = rows * (page - 1)
    end = start + rows
    # получаем отфильтрованый QuerySet
    query = get_filtered_query_set(model, request)
    # получаем список полей модели для отображения
    fields = get_model_columns([], model)
    for item in query[start:end]:
        object = {'id': item.pk}
        for field in fields:
            object[field['prefix'].replace('.', '__') + field['name']] = get_value(item, field['prefix'] + field[
                'name'])
        if func:
            object = func(object, item)
        objects.append(object)
    data = {"total": query.count(), "rows": objects}
    return HttpResponse(json.dumps(data, default=datetime_handler), content_type='application/json')


def get_filtered_query_set(model, request):
    """
    Метод создает QuerySet по указанной модели, применяет к ней фильтрации, сортировки по переданным правилам
    :param model: Модель, по которой создается QuerySet
    :param request: POST request, полученный от EasyUI DataGrid
    :return: QuerySet
    """
    # фильтрация
    if 'filterRules' in request.POST:
        # [{"field":"name","op":"contains","value":"org"}]
        rules = json.loads(request.POST['filterRules'])
    else:
        rules = None
    # сортировка
    if "sort" in request.POST:
        sort = request.POST['sort']
        order = request.POST['order']
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
        field = field+'__range'
    elif rule['op'] == 'contains':
        field = field+'__icontains'
    elif rule['op'] == 'less':
        field = field+'__lt'
    elif rule['op'] == 'greater':
        field = field+'__gt'
    query = query.filter(Q(**{field: criteria}))
    return query


def datetime_handler(obj):
    """Приводит дату в формат %d.%m.%Y"""
    if isinstance(obj, (datetime, date)):
        return obj.strftime('%d.%m.%Y')
        # return obj.isoformat()


def get_value(item, field):
    """
    Метод позволяет получить строковое значение у объекта item, хранящееся в поле field.
    :param item: Объект
    :param field: Название поля, может быть в виде "nested_object.field" с любым уровнем вложения
    :return: Строковое значение поля
    """
    val = item
    for p in str(field).split('.'):
        if val is None:
            continue
        # print("От %s берем %s" % (val, p))
        val = val.__getattribute__(p)
    if val is None:
        return None
    return str(val)


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
        try:
            if field.__class__ == fields.AutoField or \
                    field.__class__ == models.OneToOneField:
                continue
            if field.__class__ == fields.related.ForeignKey or \
                    field.__class__ == fields.related.ManyToManyRel:
                field_list = get_model_columns(field_list, field.related_model, prefix + field.name + '.', field.verbose_name)
            else:
                if field.name == 'text':
                    field_verbose_name = parent_verbose_name
                else:
                    field_verbose_name = field.verbose_name
            field_list.append({'verbose_name': field_verbose_name, 'name': field.name, 'prefix': prefix, 'field': field})
        except AttributeError:
            pass
    return field_list
