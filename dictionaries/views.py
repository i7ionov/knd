from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import simplejson as json
from django.http import HttpResponse
from dictionaries.models import House


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
    uid = request.POST['data[]']
    context = {'uid': uid}
    return render(request, 'dictionaries/address_select.html', context)
