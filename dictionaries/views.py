from datetime import datetime, timedelta
import string
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required, permission_required
import simplejson as json
from django.http import HttpResponse

from dictionaries.forms import OrganizationForm, HouseForm
from dictionaries.models import House, Address, Document, File, WorkingDays, Organization
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from dictionaries.tools import normalize_house_number
from iggn_tools import filter, messages
import uuid
from django.utils import timezone
import calendar
from django.db.models import Q


@login_required
@require_POST
@csrf_exempt
def addr_from_id_list(request):
    result = []
    for house_id in request.POST.getlist('data[]'):
        result.append([house_id, House.objects.get(pk=house_id).__str__()])
    return HttpResponse(json.dumps({'result': result}), content_type='application/json')


@login_required
@require_POST
@csrf_exempt
def addr_select(request):
    uid = request.POST['uid']
    name = request.POST['name']
    context = {'name': name, 'uid': uid}
    return render(request, 'dictionaries/address_select.html', context)


@login_required
@csrf_exempt
def addr_table_json(request):
    return filter.filtered_table_json_response(request, Address)


@require_GET
@login_required
def addr_table(request):
    context = {}
    try:
        context['uid'] = request.GET['uid']
    except MultiValueDictKeyError:
        context['uid'] = uuid.uuid1().hex
    return render(request, 'dictionaries/address_table.html', context)


@login_required
@require_POST
@csrf_exempt
def get_house_id(request):
    addr = Address.objects.get(pk=request.POST['addr_id'])
    house_number = normalize_house_number(request.POST['house_number'])
    house, created = House.objects.get_or_create(address=addr, number=house_number)
    result = {'result': house.pk}
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_required
@require_POST
@csrf_exempt
def get_houses_numbers(request, addr_id):
    data = []
    for h in House.objects.filter(address_id=addr_id):
        data.append({"text": h.number, "id": h.pk})
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def working_day_calendar(request):
    year = timezone.now().year
    context = {'year': year, 'uid': uuid.uuid1().hex}
    return render(request, 'dictionaries/working_day_calendar.html', context)


@login_required
def working_day_year(request, year):
    weeks = range(1, 6)  # количество недель
    days_in_week = range(1, 8)  # количество дней в неделе
    cal = []
    working_days = WorkingDays.objects.all()  # TODO: выгрузка только года
    for i in range(1, 13):
        cal.append(calendar.monthcalendar(year, i))
    context = {'calendar': cal, 'weeks': weeks, 'days_in_week': days_in_week, 'year': year,
               'working_days': working_days, 'uid': uuid.uuid1().hex}
    return render(request, 'dictionaries/working_day_year.html', context)


@csrf_exempt
@login_required
@require_POST
def working_day_change(request):
    try:
        day = request.POST['day']
        month = request.POST['month']
        year = request.POST['year']
        status = request.POST['status']
        date = '-'.join([year, month, day])
        if status == 'true':
            wd = WorkingDays()
            wd.day = date
            wd.save()
        else:
            try:
                wd = WorkingDays.objects.get(day=date)
                wd.delete()
            except WorkingDays.DoesNotExist:
                pass
        return messages.return_success()
    except KeyError:
        return messages.return_error('В запросе передан не полный состав ключей')


@login_required
@csrf_exempt
@require_POST
def calculate_date(request):
    try:
        src_date = datetime.strptime(request.POST['src_date'], '%d.%m.%Y')
        days_count = request.POST['days_count']
        # print('Дней ' + days_count)
        td = timedelta(int(days_count))
        result = src_date + td
        # print('src_date ' + datetime.strftime(src_date, '%d.%m.%Y'))
        # print('result ' + datetime.strftime(result, '%d.%m.%Y'))
        while src_date.toordinal() <= result.toordinal():
            if WorkingDays.objects.filter(day=src_date).count() > 0:
                # print(datetime.strftime(src_date, '%d.%m.%Y') + ' weekend')
                result = result + timedelta(1)
            src_date = src_date + timedelta(1)
            # print(datetime.strftime(src_date, '%d.%m.%Y') + ' normal')
        return messages.return_success(datetime.strftime(result, '%d.%m.%Y'))
    except KeyError:
        return messages.return_error('В запросе передан не полный состав ключей')


@login_required
@require_GET
@csrf_exempt
def org_json_list(request):
    data = []
    if 'q' in request.GET:
        q = request.GET["q"]
        for elem in Organization.objects.filter(Q(name__icontains=q) | Q(inn__icontains=q)):
            data.append({"text": elem.__str__(), "id": elem.pk})
    elif 'init_id' in request.GET:
        q = request.GET["init_id"]
        try:
            if q:
                elem = Organization.objects.get(id=q)
                data.append({"text": elem.__str__(), "id": elem.pk})
        except Organization.DoesNotExist:
            pass
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
@permission_required('dictionaries.add_organization', raise_exception=True)
def new_org_form(request):
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    uid = uuid.uuid1().hex
    org = Organization()
    org.save()
    form = OrganizationForm()
    context = {'form': form, 'load_static': load_static, 'uid': uid,
               'user_has_perm_to_save': request.user.has_perm('dictionaries.change_organization'),
               'document': org}
    return render(request, 'dictionaries/org_form.html', context)


@login_required
@permission_required('dictionaries.change_organization', raise_exception=True)
@require_POST
def org_form_save(request):
    org = Organization.objects.get(pk=request.POST['pk'])
    form = OrganizationForm(request.POST, instance=org)
    if form.is_valid():
        form.save()
        return messages.return_success()
    else:
        return messages.return_form_error(form)


@login_required
@permission_required('dictionaries.view_organization', raise_exception=True)
def edit_org_form(request, id):
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    uid = uuid.uuid1().hex
    org = get_object_or_404(Organization, pk=id)
    form = OrganizationForm(instance=org)
    context = {'form': form, 'load_static': load_static, 'uid': uid,
               'user_has_perm_to_save': request.user.has_perm('dictionaries.change_organization'),
               'document': org, 'model_name': 'organization'}
    return render(request, 'dictionaries/org_form.html', context)


@login_required
@permission_required('dictionaries.view_organization', raise_exception=True)
@csrf_exempt
def org_json_table(request):
    return filter.filtered_table_json_response(request, Organization)


@login_required
@permission_required('dictionaries.view_organization', raise_exception=True)
def org_table(request):
    context = {'user_has_perm_to_add': request.user.has_perm('dictionaries.add_organization')}
    context.update(csrf(request))
    return render(request, 'dictionaries/org_table.html', context)


@login_required
@permission_required('dictionaries.add_house', raise_exception=True)
def new_house_form(request):
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    uid = uuid.uuid1().hex
    house = House()
    house.save()
    form = HouseForm()
    context = {'form': form, 'load_static': load_static, 'uid': uid,
               'user_has_perm_to_save': request.user.has_perm('dictionaries.change_house'),
               'document': house}
    return render(request, 'dictionaries/house_form.html', context)


@login_required
@permission_required('dictionaries.change_house', raise_exception=True)
@require_POST
def house_form_save(request):
    house = House.objects.get(pk=request.POST['pk'])
    form = HouseForm(request.POST, instance=house)
    if form.is_valid():
        form.save()
        history = house.history.most_recent()
        # TODO: нужно причину исключения убирать
        return messages.return_success()
    else:
        return messages.return_form_error(form)


@login_required
@permission_required('dictionaries.view_house', raise_exception=True)
def edit_house_form(request, id):
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    uid = uuid.uuid1().hex
    house = get_object_or_404(House, pk=id)
    form = HouseForm(instance=house)
    context = {'form': form, 'load_static': load_static, 'uid': uid,
               'user_has_perm_to_save': request.user.has_perm('dictionaries.change_house'),
               'document': house, 'model_name': 'house'}
    return render(request, 'dictionaries/house_form.html', context)


@login_required
@permission_required('dictionaries.view_house', raise_exception=True)
@csrf_exempt
def house_json_table(request):
    return filter.filtered_table_json_response(request, House)


@login_required
@permission_required('dictionaries.view_house', raise_exception=True)
def house_table(request):
    context = {'user_has_perm_to_add': request.user.has_perm('dictionaries.add_house')}
    context.update(csrf(request))
    return render(request, 'dictionaries/house_table.html', context)
