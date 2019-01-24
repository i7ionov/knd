import json
from django.http import HttpResponse


def return_error(error_text):
    return HttpResponse(json.dumps([{'errorMsg': error_text}]),
                        content_type='application/json')


def return_success():
    return HttpResponse(json.dumps([]), content_type='application/json')
