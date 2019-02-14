from datetime import datetime, timedelta
import string
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required, permission_required
import simplejson as json
from django.http import HttpResponse
from analytic import general_report
from dictionaries.forms import OrganizationForm
from dictionaries.models import House, Address, Document, File, WorkingDays, Organization, Department, User
from inspections.models import ControlKind
from .models import GeneralReport, AbstractItemCountInReport, ViolationInGeneralReport
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from iggn_tools import filter, messages
import uuid
from django.utils import timezone
import calendar
from django.db.models import Q


@login_required
@csrf_exempt
def general_report_table_json(request):
    # TODO: добавить в реквест фильтрацию по пользователю, чтобы отображались только отчеты пользователя и общие отчеты
    return filter.filtered_table_json_response(request, GeneralReport)


@require_GET
@login_required
def general_report_table(request):
    context = {'uid': uuid.uuid1().hex,
               'control_kinds': ControlKind.objects.all(),
               'departments': Department.objects.all()}
    return render(request, 'analytic/general_report_table.html', context)


@require_GET
@login_required
def general_report_form(request, id):
    report = GeneralReport.objects.get(id=id)
    results = AbstractItemCountInReport.objects.filter(model_name='inspection_result', report=report)
    violations = ViolationInGeneralReport.objects.filter(report=report)
    context = {'uid': uuid.uuid1().hex,
               'report': report,
               'results': results,
               'violations': violations}
    return render(request, 'analytic/general_report_form.html', context)


@login_required
@require_POST
@csrf_exempt
def new_general_report(request):
    user = User.objects.get(pk=request.user.pk)
    date_begin = datetime.strptime(request.POST['date_begin'], '%d.%m.%Y').strftime('%Y-%m-%d')
    date_end = datetime.strptime(request.POST['date_end'], '%d.%m.%Y').strftime('%Y-%m-%d')
    control_kind = request.POST['control_kind'] if request.POST['control_kind'] != '0' else None
    department = request.POST['department'] if request.POST['department'] != '0' else None
    general_report.generate_general_report_period(user.pk, date_begin, date_end, control_kind, department)
    return messages.return_success()
