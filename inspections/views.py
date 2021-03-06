from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import simplejson as json
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt

from iggn_tools.tasks import export_to_excel_from_easyui
from iggndb.model_settings import Object
from inspections.models import ControlKind, InspectionTask, InspectionResult, LegalBasis
from . import models
from dictionaries.models import Address, Organization, House, User, Document, Department, Preference
import uuid
from datetime import datetime
from sequences import get_next_value
from inspections.forms import InspectionForm, PreceptForm
from django.views.decorators.http import require_POST
from iggn_tools import filter, messages, tools
from iggndb import tasks, settings


@login_required
@permission_required('inspections.view_inspection', raise_exception=True)
def inspection_table(request):
    try:
        column_order = Preference.objects.get(user=request.user, target='inspections_table',
                                              variable='columns_order').value.split(',')
        print(column_order)
    except Preference.DoesNotExist:
        column_order = None

    context = {'departments': Department.objects.all(),
               'inspection_results': InspectionResult.objects.all(),
               'user_has_perm_to_add': request.user.has_perm('inspections.add_inspection'), 'uid': uuid.uuid1().hex,
               'column_order': column_order}
    return render(request, 'inspections/inspection_table.html', context)


@login_required
@permission_required('inspections.view_inspection', raise_exception=True)
@csrf_exempt
def inspection_list(request):
    pk = request.POST['id']
    model = request.POST['model']
    o = Object(pk, model)
    context = {'inspections': o.object.document_set.filter(doc_type='проверка')}
    return render(request, 'inspections/inspection_list.html', context)


@login_required
@permission_required('inspections.view_precept', raise_exception=True)
@csrf_exempt
def precept_list(request):
    pk = request.POST['id']
    model = request.POST['model']
    o = Object(pk, model)
    context = {'precepts': o.object.document_set.filter(doc_type='предписание')}
    return render(request, 'inspections/precept_list.html', context)


@login_required
@permission_required('inspections.add_inspection', raise_exception=True)
def new_inspection_form(request, control_kind=None, id=None):
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    uid = uuid.uuid1().hex
    insp = models.Inspection()
    insp.doc_type = 'проверка'
    insp.doc_date = datetime.now()
    if id:
        try:
            precept = models.Precept.objects.get(pk=id)
            insp.parent = precept
            insp.doc_number = tools.increment_doc_number(precept.doc_number)
            insp.legal_basis = LegalBasis.objects.get(id=4)
            insp.control_kind = precept.parent.inspection.control_kind
            insp.control_form = precept.parent.inspection.control_form
            insp.control_plan = precept.parent.inspection.control_plan
            insp.organization = precept.organization
            insp.inspector = User.objects.get(django_user=request.user)
            insp.department = insp.inspector.department
            insp.update_inspection_type()
            insp.save()
            insp.inspection_tasks.add(InspectionTask.objects.get(id=26))
            insp.houses.set(precept.houses.all())
            precept.update_days_to_start_new_inspection()
        except (KeyError, models.Precept.DoesNotExist):
            return messages.return_error(f'Не найдено предписание с id={id}')
    elif control_kind:
        insp.control_kind = ControlKind.objects.get(pk=control_kind)
        insp.doc_number = get_next_value('inspection')
        if control_kind == 2:
            insp.doc_number = str(insp.doc_number) + 'л'
        insp.inspector = User.objects.get(django_user=request.user)
        insp.department = insp.inspector.department
        insp.update_inspection_type()
        insp.save()
    form = InspectionForm(instance=insp)
    context = {'form': form, 'load_static': load_static, 'uid': uid,
               'user_has_perm_to_save': request.user.has_perm('inspections.change_inspection'),
               'document': insp, 'model_name': 'inspection'}
    return render(request, 'inspections/inspection_form.html', context)


@login_required
@permission_required('inspections.change_inspection', raise_exception=True)
@require_POST
def inspection_form_save(request):
    inspection = models.Inspection.objects.get(pk=request.POST['pk'])
    form = InspectionForm(request.POST, instance=inspection)
    if request.POST['control_form'] == '' or int(request.POST['control_form']) < 4:
        if request.POST['inspection_result'] != '12':
            if '12' not in request.POST.getlist('inspection_tasks'):  # 12 - порядок размещения инфы в ГИС ЖКХ, дома не нужны
                if len(request.POST.getlist('houses')) == 0:
                    return messages.return_error('Необходимо заполнить адреса домов')
    if form.is_valid():
        save_violations_in_inspection(request.POST.getlist('violations'), inspection)
        inspection.violations_quantity = 0
        for v in inspection.violationininspection_set.all():
            if v.violation_type.children.count() == 0:
                inspection.violations_quantity += v.count
        form.instance.department = form.instance.inspector.department
        form.save()
        return messages.return_success()
    else:
        return messages.return_form_error(form)


@login_required
@permission_required('inspections.view_inspection', raise_exception=True)
def edit_inspection_form(request, id):
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    uid = uuid.uuid1().hex
    insp = get_object_or_404(models.Inspection, pk=id)
    form = InspectionForm(instance=insp)
    user_has_perm_to_save = True
    context = {'form': form, 'load_static': load_static, 'uid': uid,
               'user_has_perm_to_save': user_has_perm_to_save,
               'document': insp, 'model_name': 'inspection'}
    return render(request, 'inspections/inspection_form.html', context)


@login_required
@permission_required('inspections.add_precept', raise_exception=True)
def new_precept_form(request, id):
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    uid = uuid.uuid1().hex
    insp = models.Inspection.objects.get(pk=id)
    precept = models.Precept()
    precept.doc_type = 'предписание'
    precept.doc_number = insp.doc_number
    precept.doc_date = datetime.now()
    precept.parent = insp
    precept.organization = insp.organization
    precept.save()
    precept.houses.set(insp.houses.all())
    form = PreceptForm(instance=precept)
    context = {'form': form, 'load_static': load_static, 'uid': uid,
               'user_has_perm_to_save': request.user.has_perm('inspections.change_precept'),
               'document': precept, 'model_name': 'precept'}
    return render(request, 'inspections/precept_form.html', context)


@login_required
@permission_required('inspections.change_precept', raise_exception=True)
@require_POST
def precept_form_save(request):
    precept = models.Precept.objects.get(pk=request.POST['pk'])
    form = PreceptForm(request.POST, instance=precept)

    if form.is_valid():
        form.save()
        precept.update_days_to_start_new_inspection()
        save_violations_in_precept(request.POST.getlist('violations'), precept)
        return messages.return_success()
    else:
        return messages.return_form_error(form)


@login_required
@permission_required('inspections.view_precept', raise_exception=True)
def edit_precept_form(request, id):
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    uid = uuid.uuid1().hex
    precept = get_object_or_404(models.Precept, pk=id)
    form = PreceptForm(instance=precept)
    user_has_perm_to_save = False
    if precept.parent.inspection.inspector == User.objects.get(django_user=request.user) or \
            request.user.has_perm('inspections.can_change_others_inspections'):
        user_has_perm_to_save = True
    context = {'form': form, 'load_static': load_static, 'uid': uid,
               'user_has_perm_to_save': user_has_perm_to_save,
               'document': precept, 'model_name': 'precept'}
    return render(request, 'inspections/precept_form.html', context)


@login_required
@csrf_exempt
def violation_in_inspection_json_list(request, id=0):
    try:
        d = models.Inspection.objects.get(id=id)
        violations = d.violationininspection_set.all()
    except (models.Inspection.DoesNotExist, ValueError):
        violations = ''
    context = {'violations': violations}
    return render(request, 'inspections/violation_in_inspection_json_list.html', context)


@login_required
@csrf_exempt
def violation_in_precept_json_list(request, id=0, parent_id=0):
    context = {}
    if id > 0:
        try:
            o = models.Precept.objects.get(id=id)
            d = models.Inspection.objects.get(id=o.parent.id)
            violations = []
            for v_in_d in d.violationininspection_set.all():
                if o.violationinprecept_set.filter(violation_type_id=v_in_d.violation_type_id).exists():
                    v_in_o = o.violationinprecept_set.get(violation_type_id=v_in_d.violation_type_id)
                else:
                    v_in_o = models.ViolationInPrecept()
                item = {
                    'count_to_remove': v_in_o.count_to_remove,
                    'count_of_removed': v_in_o.count_of_removed,
                    'count_in_inspection': v_in_d.count - v_in_d.count_has_precept + v_in_o.count_to_remove,
                    'violation_type_id': v_in_d.violation_type_id,
                }
                violations.append(item)
        except (models.Precept.DoesNotExist, models.Inspection.DoesNotExist, ValueError):
            violations = ''
        context = {'violations': violations, 'is_new_instance': False}
    elif parent_id > 0:
        try:
            d = models.Inspection.objects.get(id=parent_id)
            violations = d.violationininspection_set.all()
        except (models.Inspection.DoesNotExist, ValueError):
            violations = ''
        context = {'violations': violations, 'is_new_instance': True}
    return render(request, 'inspections/violation_in_precept_json_list.html', context)


@login_required
@permission_required('inspections.view_inspection', raise_exception=True)
@csrf_exempt
def inspection_json_table(request):
    # сразу смотрим, если это задача экспорта в Excel, то передаем ее в соответствующую функцию
    if 'excel' in request.POST and request.POST['excel']:
        if settings.DEBUG:
            export_to_excel_from_easyui(request.POST, 'inspections', 'Inspection', request.user.id, get_count=False)
        else:
            export_to_excel_from_easyui.delay(request.POST, 'inspections', 'Inspection', request.user.id, get_count=False)
    return filter.filtered_table_json_response(request, models.Inspection, additional_fields_for_inspection)


@login_required
@permission_required('django_celery_beat.add_periodictask', raise_exception=True)
def start_import(request):
    tasks.import_from_gis_gkh.delay()
    return HttpResponse(json.dumps([]), content_type='application/json')


def additional_fields_for_inspection(object, item):
    # Задачи проверки
    task = InspectionTask.objects.filter(inspection__id=item.id).first()
    if task is not None:
        object['inspection_tasks__text'] = task.text
    # Адрес
    house = House.objects.filter(document__id=item.id).first()
    if house is not None:
        object['houses__address__city'] = house.address.city
        object['houses__address__street'] = house.address.street
        object['houses__number'] = house.number
    # Нарушения
    violations = ''
    for v in item.violationininspection_set.all():
        if v.violation_type.children.count() == 0:
            if v.violation_type.parent:
                violations = f'{violations} {v.violation_type.parent.text} {v.violation_type.text};'
            else:
                violations = f'{violations} {v.violation_type.text};'
    object['violationininspection__violation_type__text'] = violations
    # Предписание
    precept = models.Precept.objects.filter(parent_id=item.id).first()
    if precept is not None:
        object['children__doc_number'] = precept.doc_number
        object['children__doc_date'] = precept.doc_date
        object['children__precept__precept_begin_date'] = precept.precept_begin_date
        object['children__precept__precept_end_date'] = precept.precept_end_date
        if precept.precept_result:
            object['children__precept__precept_result__id'] = precept.precept_result.text
        object['children__precept__days_to_start_new_inspection'] = precept.days_to_start_new_inspection
    return object


def save_violations_in_inspection(violations, inspection):
    """Сохраняет нарушения, выявленные в ходе проверки.
    :param violations: Список строк, содержащий id типа нарушения и количества нарушений, разделенных точкой с запятой
    """
    for v in violations:
        v_id = str(v).split(';')[0]
        v_count = str(v).split(';')[1]
        if str(v_count) == 'undefined' or str(v_count) == '':
            inspection.violationininspection_set.filter(violation_type_id=v_id).delete()
            continue
        if int(v_count) > 0:
            try:
                violation, created = models.ViolationInInspection.objects.get_or_create(violation_type_id=v_id,
                                                                                        inspection=inspection)
            except models.ViolationInInspection.MultipleObjectsReturned:
                inspection.violationininspection_set.filter(violation_type_id=v_id).delete()
                violation, created = models.ViolationInInspection.objects.get_or_create(violation_type_id=v_id,
                                                                                        inspection=inspection)
            if violation.violation_type.parent is None:
                inspection.violations_quantity = int(v_count)
            violation.count = v_count
            violation.save()

        else:
            inspection.violationininspection_set.filter(violation_type_id=v_id).delete()


def save_violations_in_precept(violations, precept):
    """Сохраняет информациию по нарушениям в предписании.
    :param violations: Список строк, содержащий id типа нарушения и количества выявленных нарушений и количества нарушений к исправлению, разделенных точкой с запятой
    """
    for v in violations:
        v_id = str(v).split(';')[0]
        v_count_to_remove = str(v).split(';')[1]
        v_count_of_removed = str(v).split(';')[2]
        # если не указано количество нарушений к устранению, то вообще пропускаем это нарушение
        if str(v_count_to_remove) == 'undefined' or str(v_count_to_remove) == '':
            precept.violationinprecept_set.filter(violation_type_id=v_id).delete()
            continue
        if int(v_count_to_remove) > 0:
            try:
                violation, created = models.ViolationInPrecept.objects.get_or_create(violation_type_id=v_id,
                                                                                     precept=precept)
                violation.count_to_remove = int(v_count_to_remove)
            except models.ViolationInPrecept.MultipleObjectsReturned:
                precept.violationinprecept_set.filter(violation_type_id=v_id).delete()
                violation, created = models.ViolationInPrecept.objects.get_or_create(violation_type_id=v_id,
                                                                                     precept=precept)
            if str(v_count_of_removed) == 'undefined' or str(v_count_of_removed) == '':
                pass
            else:
                violation.count_of_removed = int(v_count_of_removed)
            violation.save()

        else:
            precept.violationinprecept_set.filter(violation_type_id=v_id).delete()
