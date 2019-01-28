from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import uuid
from dictionaries.models import Document
from ad.models import ADStage
from iggn_tools import messages
from inspections.forms import InspectionForm, PreceptForm


@login_required
def index(request):
    context = {}
    return render(request, 'index.html', context)


@login_required
@csrf_exempt
@require_POST
def history_table(request):
    try:
        id = request.POST['id']
        d = Document.objects.get(id=id)
        if d.doc_type == 'проверка':
            history = d.inspection.history.all()
        if d.doc_type == 'предписание':
            history = d.precept.history.all()
        if d.doc_type == 'административное дело':
            history = d.adrecord.history.all()
    except (Document.DoesNotExist, ValueError):
        history = ''
    context = {'history': history}
    return render(request, 'history/history_table.html', context)


@login_required
def history_form(request, id, history_id):
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    uid = uuid.uuid1().hex
    d = Document.objects.get(id=id)
    if d.doc_type == 'проверка':
        insp = d.inspection.history.get(history_id=history_id)
        form = InspectionForm(instance=insp)
        context = {'form': form, 'load_static': load_static, 'uid': uid,
                   'user_has_perm_to_save': False,
                   'document': insp}
        return render(request, 'inspections/inspection_form.html', context)
    elif d.doc_type == 'предписание':
        precept = d.precept.history.get(history_id=history_id)
        form = PreceptForm(instance=precept)
        context = {'form': form, 'load_static': load_static, 'uid': uid,
                   'user_has_perm_to_save': False,
                   'document': precept}
        return render(request, 'inspections/precept_form.html', context)
    return ''


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
         'ad_stage_list': ADStage.objects.all()
    }
    return render(request, 'document_tree/document_tree.html', context)
