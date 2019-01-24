from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required, permission_required
import simplejson as json
from django.http import HttpResponse
from dictionaries.models import House, Address, Document, File
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from iggn_tools import filter, messages
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


@csrf_exempt
@login_required
def file_select(request):
    context = {}
    if request.method == 'POST':
        context = {
            'parent_id': request.POST['parent_id'],
            'uid': request.POST['uid'],
        }
    context.update(csrf(request))
    return render(request, 'dictionaries/file_select.html', context)


@csrf_exempt
@login_required
@permission_required('dictionaries.view_file', raise_exception=True)
@require_POST
def files_list(request):
    uid = request.POST['uid']
    id = request.POST['id']
    if id == "None":
        return messages.return_error("Нет id документа")
    try:
        document = Document.objects.get(pk=id)
    except (KeyError, Document.DoesNotExist):
        return messages.return_error("Нет документа с таким id")
    context = {
        'document': document,
        'uid': uid,
        'files': document.files.all(),
    }
    return render(request, 'dictionaries/files_list.html', context)


@csrf_exempt
@login_required
@permission_required('dictionaries.add_file', raise_exception=True)
@require_POST
def file_add(request):
    try:
        parent_id = request.POST['parent_id']
        document = Document.objects.get(pk=parent_id)
    except Document.DoesNotExist:
        return messages.return_error('Не найден документ, к которому должен быть прикреплен файл')
    try:
        file = File()
        myfile = request.FILES['file']
        fs = FileSystemStorage(
            location='{0}/{1}/{2}{3}'.format(settings.MEDIA_ROOT, document.doc_type, document.doc_number,
                                             document.doc_date),
            base_url='/media/{0}/{1}{2}'.format(document.doc_type, document.doc_number, document.doc_date))
        filename = fs.save(myfile.name.replace(' ', '_'), myfile)
        file.name = myfile.name
        file.path = fs.url(filename)
    except KeyError:
        return messages.return_error('Не была передана чаcть параметров')
    file.save()
    document.files.add(file)
    document.save()
    return messages.return_success()
