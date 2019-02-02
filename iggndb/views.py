from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import uuid
from dictionaries.models import Document, Organization, File
from iggndb import settings
from iggndb.model_settings import Object
from inspections.models import Inspection, Precept
from ad.models import ADStage, ADRecord
from iggn_tools import messages
from inspections.forms import InspectionForm, PreceptForm
from ad.forms import ADRecordForm
from dictionaries.forms import OrganizationForm


@login_required
def index(request):
    context = {}
    return render(request, 'index.html', context)


@login_required
@csrf_exempt
@require_POST
def history_table(request):
    id = request.POST['id']
    model = request.POST['model']
    d = None
    history = None
    d = Object(id, model)
    if d:
        history = d.object.history.all()
    context = {'history': history, 'model': model}
    return render(request, 'history/history_table.html', context)


@login_required
def history_form(request, id, history_id, model):
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    uid = uuid.uuid1().hex
    o = Object(id, model)
    history = o.object.history.get(history_id=history_id)
    form = o.form(instance=history)
    context = {'form': form, 'load_static': load_static, 'uid': uid,
               'user_has_perm_to_save': False,
               'document': history, 'model': model}
    return render(request, o.template, context)


@login_required
@csrf_exempt
def document_tree_json(request, id=0):
    doc = Document.objects.get(id=id)
    documents = Document.objects.filter(tree_id=doc.tree_id)
    context = {'documents': documents}
    return render(request, 'document_tree/document_tree_json.html', context)


@login_required
@csrf_exempt
@require_POST
def document_tree(request, id=0):
    id = request.POST['id']
    if id == "None":
        return messages.return_error('Id=None')
    uid = request.POST['uid']
    try:
        document = Document.objects.get(pk=id)
    except (KeyError, Document.DoesNotExist):
        return messages.return_error('Документ не найден')
    context = {
        'document': document,
        'uid': uid,
        'user_has_perm_to_add_adrecord': request.user.has_perm('ad.add_adrecord'),
         'ad_stage_list': ADStage.objects.all()
    }
    return render(request, 'document_tree/document_tree.html', context)


@csrf_exempt
@login_required
@require_POST
def file_select(request):

    context = {
        'parent_id': request.POST['parent_id'],
        'model': request.POST['model'],
        'uid': request.POST['uid'],
    }
    context.update(csrf(request))
    return render(request, 'files/file_select.html', context)


@csrf_exempt
@login_required
@permission_required('dictionaries.view_file', raise_exception=True)
@require_POST
def files_list(request):
    uid = request.POST['uid']
    id = request.POST['id']
    model = request.POST['model']
    if id == "None":
        return messages.return_error("Нет id документа")
    o = Object(id, model)
    context = {
        'document': o.object,
        'uid': uid,
        'model': model,
        'files': o.object.files.all(),
    }
    return render(request, 'files/files_list.html', context)


@csrf_exempt
@login_required
@permission_required('dictionaries.add_file', raise_exception=True)
@require_POST
def file_add(request):
    parent_id = request.POST['parent_id']
    model = request.POST['model']
    o = Object(parent_id, model)
    try:
        file = File()
        myfile = request.FILES['file']
        fs = FileSystemStorage(
            location=o.file_location,
            base_url=o.base_file_url)
        filename = fs.save(myfile.name.replace(' ', '_'), myfile)
        file.name = myfile.name
        file.path = fs.url(filename)
    except KeyError:
        return messages.return_error('Не была передана чаcть параметров')
    file.save()
    o.object.files.add(file)
    o.object.save()
    return messages.return_success()
