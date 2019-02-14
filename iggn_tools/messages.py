import json
from django.http import HttpResponse


def return_error(error_text):
    return HttpResponse(json.dumps([{'errorMsg': error_text}]),
                        content_type='application/json')


def return_success(message=None):

    data = [{'msg': message if message else ''}]
    return HttpResponse(json.dumps(data), content_type='application/json')


def return_form_error(form):
    error = ''
    for field in list(form.errors):
        label = form.fields[field].label
        for er in list(form.errors[field]):
            error += f'{label}: {er}'
    return return_error(error)