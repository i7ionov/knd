from django.shortcuts import render
from django.http import HttpResponse
import simplejson as json
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from . import models
from dictionaries.models import Address, Organization, House, User
import uuid
from datetime import datetime
from sequences import get_next_value
from inspections.forms import InspectionForm


@login_required
@permission_required('inspections.view_inspection', raise_exception=True)
def inspection_table(request):
    context = {'user_has_perm_to_add': request.user.has_perm('inspections.add_inspection')}
    context.update(csrf(request))
    return render(request, 'inspections/inspection_table.html', context)


@login_required
@permission_required('inspections.add_inspection', raise_exception=True)
def new_inspection_form(request):
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    insp = models.Inspection()
    insp.doc_number = get_next_value('inspection')
    insp.doc_date = datetime.now()
    insp.inspector = User.objects.get(django_user=request.user)
    insp.save()
    form = InspectionForm(prefix=uuid.uuid1().hex, instance=insp)
    context = {'form': form, 'load_static': load_static}
    return render(request, 'inspections/inspection_form.html', context)
