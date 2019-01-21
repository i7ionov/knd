"""������ �������� ������ ��� ������������ QuerySet'��"""
import simplejson as json
import django
from datetime import date, datetime
from django.db.models import fields
from django.db.models import Q
from django.db import models


def filtered_table_json_response(request, model):
    """����� ������� ������� JSON ����� �� request, ������������ EasyUI DataGrid.
    Response �������� �������������� �� ��������� ������� ��������� ������."""
    objects = []
    # ���������
    page = 1
    rows = 10
    if "page" in request.POST:
        page = int(request.POST['page'])
    if "rows" in request.POST:
        rows = int(request.POST['rows'])
    start = rows * (page - 1)
    end = start + rows
    # �������� �������������� QuerySet
    query = get_filtered_query_set(model, request)
    # �������� ������ ����� ������ ��� �����������
    fields = get_model_columns([], model)

    for item in query[start:end]:
        object = {'id': item.pk}
        for field in fields:
            object[field['prefix'].replace('.', '__') + field['name']] = get_value(item, field['prefix'] + field[
                'name'])
        objects.append(object)
    data = {"total": model.objects.all().count(), "rows": objects}
    return json.dumps(data, default=datetime_handler)


def get_filtered_query_set(model, request):
    """
    ����� ������� QuerySet �� ��������� ������, ��������� � ��� ����������, ���������� �� ���������� ��������
    :param model: ������, �� ������� ��������� QuerySet
    :param request: POST request, ���������� �� EasyUI DataGrid
    :return: QuerySet
    """
    # ����������
    if 'filterRules' in request.POST:
        # [{"field":"name","op":"contains","value":"org"}]
        rules = json.loads(request.POST['filterRules'])
    else:
        rules = None
    # ����������
    if "sort" in request.POST:
        print(request.POST['sort'])
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
    ����� ������� QuerySet �� ��������� ������, ��������� � ��� ���������� �� ���� ���������� ��������
    :param model: ������, �� ������� ��������� QuerySet
    :param rules: ������ ������ ��� ���������� � ���� �������, ����������������� �� JSON.
    ������: [{"nested_object__field":"name","op":"contains","value":"org"}],

    ���� op ����� ��������� ��������� ��������: contains, less, greater
    :return: QuerySet � ����������� �����������
    """
    query = model.objects.all()
    if rules:
        for rule in rules:
            query = add_filter_from_easyui(query, rule)
    return query


def add_filter_from_easyui(query, rule):
    """
    ����� ��������� ���������� � ����������� QuerySet �� ��������� �������
    :param query: QuerySet
    :param rule: ������� ��� ���������� � ���� �������, ����������������� �� JSON.
    ������: [{"field":"name","op":"contains","value":"org"}].
    ���� op ����� ��������� ��������� ��������: contains, less, greater
    :return: QuerySet � ����������� �����������
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
    """�������� ���� � ������ %d.%m.%Y"""
    if isinstance(obj, (datetime, date)):
        return obj.strftime('%d.%m.%Y')
        # return obj.isoformat()


def get_value(item, field):
    """
    ����� ��������� �������� ��������� �������� � ������� item, ���������� � ���� field.
    :param item: ������
    :param field: �������� ����, ����� ���� � ���� "nested_object.field" � ����� ������� ��������
    :return: ��������� �������� ����
    """
    val = item
    for p in str(field).split('.'):
        if val is None:
            continue
        # print("�� %s ����� %s" % (val, p))
        val = val.__getattribute__(p)
    if val is None:
        return None
    return str(val)


def get_model_columns(field_list, model, prefix='', parent_verbose_name=''):
    """
    ����� ������� ������ ����� � ������� ���� ���������� verbose_name, �������� ����������.
    :param field_list: ������ � ������: verbose_name, name, prefix, field
    :param model: ������, ���� ������� ����� ��������
    :param prefix: ������� ��� ����. ������������ � ��������� ��������. ������ ��� ������������� ����
    :param parent_verbose_name: ������������ � ��������� ��������. ������ ���������������� ��������
    ������������� ����
    :return: ���������� ������ �������� � ������:
    verbose_name - ���������������� �������� ����,
    name - ��� ����,
    prefix - ��� ������������� ���� � ������ �� �����,
    field - ������ �� ��� ������ ����
    """
    # ������� ���� � verbose_name
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
