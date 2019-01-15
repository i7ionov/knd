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


@login_required
@permission_required('inspections.view_inspection', raise_exception=True)
def inspection_table(request):
    context = {'user_has_perm_to_add': request.user.has_perm('inspections.add_inspection')}
    context.update(csrf(request))
    return render(request, 'inspections/inspection_table.html', context)

