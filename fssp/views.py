import json
from urllib.parse import urlencode

import requests
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from fssp import models
from fssp.models import Request, Response
from iggn_tools import filter, messages, tools

@login_required
@permission_required('fssp.view_requests', raise_exception=True)
@csrf_exempt
def request_json_table(request):
    return filter.filtered_table_json_response(request, models.Request)


@csrf_exempt
def fssp_query_form(request):
    return render(request, 'fssp/fssp_query_form.html')


@csrf_exempt
def fssp_search_legal(request):
    if request.POST:
        data = dict(request.POST)
        data['region'] = 59
        data['token'] = data['token'][0]
        data['name'] = data['name'][0]
        resp = requests.get('https://api-ip.fssp.gov.ru/api/v1.0/search/legal/',params=urlencode(data))
        #resp = requests.get('http://127.0.0.1:8000/sdf/', params=urlencode(data))
        resp_data = json.loads(resp.text)
        if resp_data['code'] == 0:
            Request(task=resp_data["response"]["task"],
                    token=data['token'],
                    type='search_legal',
                    text=f'Поиск сведений о {data["name"]}').save()
        return JsonResponse(resp_data)
    return render(request, 'fssp/search_legal.html')


@csrf_exempt
def requests_table(request):
    return render(request, 'fssp/requests_table.html')


@csrf_exempt
def response(request,id):
    req = Request.objects.get(id=id)
    context = {'task':req.task, 'token': req.token}
    return render(request, 'fssp/response_form.html', context=context)


@csrf_exempt
def result(request):
    if request.POST:
        data = dict(request.POST)
        data['token'] = data['token'][0]
        data['task'] = data['task'][0]
        resp = requests.get('https://api-ip.fssp.gov.ru/api/v1.0/result/', params=urlencode(data))
        resp_data = json.loads(resp.text)
        if resp_data['code'] == 0 and resp_data["response"]['status'] == 0:
            for result in resp_data["response"]['result'][0]['result']:

                print(result['name'])
            #Response(name=resp_data["response"]["task"])
        return JsonResponse(resp_data)