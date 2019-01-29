from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import uuid
from dictionaries.models import Document, Organization
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
    if model == 'organization':
        d = Organization.objects.get(id=id)
    elif model == 'inspection':
        d = Inspection.objects.get(id=id)
    elif model == 'precept':
        d = Precept.objects.get(id=id)
    elif model == 'ad_record':
        d = ADRecord.objects.get(id=id)
    if d:
        history = d.history.all()
    context = {'history': history, 'model': model}
    return render(request, 'history/history_table.html', context)


@login_required
def history_form(request, id, history_id, model):
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    uid = uuid.uuid1().hex
    template = None
    base_form = None
    if model == 'inspection':
        d = Inspection.objects.get(id=id)
        base_form = InspectionForm
        template = 'inspections/inspection_form.html'
    elif model == 'precept':
        d = Precept.objects.get(id=id)
        base_form = PreceptForm
        template = 'inspections/precept_form.html'
    elif model == 'ad_record':
        d = ADRecord.objects.get(id=id)
        base_form = ADRecordForm
        template = 'ad/ad_record_form.html'
    elif model == 'organization':
        d = Organization.objects.get(id=id)
        base_form = OrganizationForm
        template = 'dictionaries/org_form.html'
    history = d.history.get(history_id=history_id)
    form = base_form(instance=history)
    context = {'form': form, 'load_static': load_static, 'uid': uid,
               'user_has_perm_to_save': False,
               'document': history, 'model': model}
    return render(request, template, context)



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
