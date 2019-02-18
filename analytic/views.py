from datetime import datetime, timedelta
import string
from django.apps import apps
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required, permission_required
import simplejson as json
from django.http import HttpResponse
import iggn_tools
from analytic import general_report, tasks
from analytic.tools import convert_request
from dictionaries.forms import OrganizationForm
from dictionaries.models import House, Address, Document, File, WorkingDays, Organization, Department, User
from inspections.models import ControlKind
from .models import GeneralReport, AbstractItemCountInReport, ViolationInGeneralReport, ExportResult
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from iggn_tools import filter, messages
import uuid
from django.utils import timezone
import calendar
from django.db.models import Q


@login_required
@csrf_exempt
def general_report_table_json(request):
    rules = [{'field': 'user__django_user__id', 'op': 'equals', 'value': request.user.id}]
    return filter.filtered_table_json_response(request, GeneralReport, filtering_rules=rules)


@require_GET
@login_required
def general_report_table(request):
    context = {'uid': uuid.uuid1().hex,
               'control_kinds': ControlKind.objects.all(),
               'departments': Department.objects.all()}
    return render(request, 'analytic/general_report_table.html', context)


@require_GET
@login_required
def general_report_form(request, id):
    report = GeneralReport.objects.get(id=id)
    results = AbstractItemCountInReport.objects.filter(model_name='inspection_result', report=report)
    violations = ViolationInGeneralReport.objects.filter(report=report)
    context = {'uid': uuid.uuid1().hex,
               'report': report,
               'results': results,
               'violations': violations}
    return render(request, 'analytic/general_report_form.html', context)


@login_required
@require_POST
@csrf_exempt
def new_general_report(request):
    user = User.objects.get(pk=request.user.pk)
    date_begin = datetime.strptime(request.POST['date_begin'], '%d.%m.%Y').strftime('%Y-%m-%d')
    date_end = datetime.strptime(request.POST['date_end'], '%d.%m.%Y').strftime('%Y-%m-%d')
    control_kind = request.POST['control_kind'] if request.POST['control_kind'] != '0' else None
    department = request.POST['department'] if request.POST['department'] != '0' else None
    tasks.generate_general_report_period(user.pk, date_begin, date_end, control_kind, department)
    return messages.return_success()


@csrf_exempt
@login_required
def filter_form(request):
    if request.GET['app'] and request.GET['model']:
        app_str = request.GET['app']
        model_str = request.GET['model']
    else:
        return messages.return_error('Ошибка запроса')
    if request.GET.get('get_count', False):
        get_count = True
    else:
        get_count = False
    if request.method == 'POST':
        request_post = convert_request(request)
        if get_count:
            return tasks.export_to_excel(request_post, app_str, model_str, request.user.pk, True)
        else:
            tasks.export_to_excel.delay(request_post, app_str, model_str, request.user.pk, False)
            return messages.return_success()
    else:
        if request.GET['uid']:
            uid = request.GET['uid']
        else:
            uid = uuid.uuid1().hex
        context = {
            'uid': uuid.uuid1().hex,
            'app': app_str,
            'model': model_str,
            'fields': iggn_tools.filter.get_model_columns([], apps.get_model(app_str, model_str))
        }
        return render(request, 'analytic/filter_form.html', context)


@login_required
@csrf_exempt
def field_filter_form(request):
    if request.GET['app'] and request.GET['model']:
        app_str = request.GET['app']
        model_str = request.GET['model']
    else:
        return messages.return_error('Ошибка запроса')
    model = apps.get_model(app_str, model_str)
    fields = str(request.POST['field']).split('.')
    if fields[0] != 'none':
        field_name = ''
        for f in fields:
            field = model._meta.get_field(f)
            model = field.related_model
            if field_name:
                field_name = field_name + '__' + field.name
            else:
                field_name = field.name
    else:
        field_name = model_str
        field = model
    context = {'field': field, 'uid': uuid.uuid1().hex, 'field_class': str(field.__class__), 'field_name': field_name,
               'app': app_str, 'model': model_str}
    return render(request, 'analytic/field_filter_form.html', context)


@login_required
@csrf_exempt
def generic_json_list(request):
    """
    Метод обеспечивает автозаполнение для типовых тектовых полей.
    :param request: GET-request c параметрами app, model, field и q
    :return: Возвращает в формате JSON 10 первых уникальных значений модели model в приложении app по полю field,
    содержащих в себе значение q
    """
    data = []
    if request.method == 'GET':
        if request.GET['app'] and request.GET['model']:
            app_str = request.GET['app']
            model_str = request.GET['model']
            field_str = request.GET['field']
            model = apps.get_model(app_str, model_str)
        else:
            return HttpResponse(json.dumps([{'error': 'error'}]), content_type='application/json')
        try:
            q = request.GET["q"]
        except KeyError:
            q = ''
        for elem in model.objects.filter(Q(**{field_str+"__icontains": q})).order_by(field_str).distinct(field_str)[:10]:
            f = elem
            for p in field_str.split('__'):
                if f is None:
                    continue
                f = f.__getattribute__(p)
            data.append({"text": f, "id": elem.pk})
    return HttpResponse(json.dumps(data), content_type='application/json')


@require_GET
@login_required
def excel_export_table(request):
    context = {'uid': uuid.uuid1().hex,
               'results': ExportResult.objects.filter(user=request.user.pk).order_by('-id')}
    return render(request, 'analytic/excel_export_table.html', context)
