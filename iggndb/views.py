from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import uuid
from dictionaries.models import Document
from inspections.forms import InspectionForm

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
    return ''
