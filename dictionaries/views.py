from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import simplejson as json
from django.http import HttpResponse
from dictionaries.models import House, Address
from iggn_tools import filter
import uuid


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
    return HttpResponse(filter.filtered_table_json_response(request, Address), content_type='application/json')


@require_GET
@login_required
def addr_table(request):
    context = {}
    try:
        context['uid'] = request.GET['uid']
    except ():
        context['uid'] = uuid.uuid1().hex
    return render(request, 'dictionaries/address_table.html', context)


@login_required
@require_POST
@csrf_exempt
def get_house_id(request):
    addr = Address.objects.get(pk=request.POST['addr_id'])
    house_number = request.POST['house_number']
    house, created = House.objects.get_or_create(address=addr, number=house_number)
    result = {'result': house.pk}
    return HttpResponse(json.dumps(result), content_type='application/json')
