from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import simplejson as json
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from . import models
from dictionaries.models import Address, Organization, House, User
import uuid
from datetime import datetime
from sequences import get_next_value
from inspections.forms import InspectionForm
from django.views.decorators.http import require_POST
from iggn_tools import filter


@login_required
@permission_required('inspections.view_inspection', raise_exception=True)
def inspection_table(request):
    context = {'user_has_perm_to_add': request.user.has_perm('inspections.add_inspection')}
    context.update(csrf(request))
    return render(request, 'inspections/inspection_table.html', context)


@login_required
@permission_required('inspections.add_inspection', raise_exception=True)
def new_inspection_form(request):
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    uid = uuid.uuid1().hex
    insp = models.Inspection()
    insp.doc_number = get_next_value('inspection')
    insp.doc_date = datetime.now()
    insp.inspector = User.objects.get(django_user=request.user)
    insp.save()
    form = InspectionForm(instance=insp)
    context = {'form': form, 'load_static': load_static, 'uid': uid,
               'user_has_perm_to_save': request.user.has_perm('inspections.change_inspection'),
               'inspection': insp}
    return render(request, 'inspections/inspection_form.html', context)


@login_required
@permission_required('inspections.change_inspection', raise_exception=True)
@require_POST
def inspection_form_save(request):
    inspection = models.Inspection.objects.get(pk=request.POST['pk'])
    form = InspectionForm(request.POST, instance=inspection)
    if form.is_valid():
        form.save()
        save_violations_in_inspection(request.POST.getlist('violations'), inspection)
        return HttpResponse(json.dumps([{'result': 'Форма успешно сохранена'}]), content_type='application/json')
    else:
        return HttpResponse(json.dumps([{'result': form.errors}]), content_type='application/json')


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
@permission_required('inspections.view_inspection', raise_exception=True)
def edit_inspection_form(request, id):
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    uid = uuid.uuid1().hex
    insp = get_object_or_404(models.Inspection, pk=id)
    form = InspectionForm(instance=insp)
    context = {'form': form, 'load_static': load_static, 'uid': uid,
               'user_has_perm_to_save': request.user.has_perm('inspections.change_inspection'),
               'inspection': insp}
    return render(request, 'inspections/inspection_form.html', context)


@login_required
@permission_required('inspections.view_inspection', raise_exception=True)
@csrf_exempt
def inspection_json_table(request):
    print(request.POST)
    return HttpResponse(
        filter.filtered_table_json_response(request, models.Inspection, additional_fields_for_inspection))


def additional_fields_for_inspection(object, item):
    # Адрес
    house = House.objects.filter(document__id=item.id).first()
    if house is not None:
        object['houses__address__city'] = house.address.city
        object['houses__address__street'] = house.address.street
        object['houses__number'] = house.number
    # Предписание
    order = models.Order.objects.filter(parent_id=item.id).first()
    if order is not None:
        object['children__doc_number'] = order.doc_number
        object['children__doc_date'] = order.doc_date
        object['children__order__order_result__id'] = order.order_result.text
    return object

def save_violations_in_inspection(violations, inspection):
    """Сохраняет нарушения, выявленные в ходе проверки.
    :param violations: Список строк, содержащий id типа нарушения и количества нарушений, разделенных точкой с запятой
    """
    for v in violations:
        v_id = str(v).split(';')[0]
        v_count = str(v).split(';')[1]
        if str(v_count) == 'undefined' or str(v_count) == '':
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