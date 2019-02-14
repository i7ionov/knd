from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import simplejson as json
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt

from iggndb.model_settings import Object
from . import models
from dictionaries.models import Address, Organization, House, User, Document
import uuid
from datetime import datetime
from sequences import get_next_value
from ad.forms import ADRecordForm
from django.views.decorators.http import require_POST
from iggn_tools import filter, messages, tools


@login_required
@permission_required('ad.add_adrecord', raise_exception=True)
def new_ad_record_form(request, ad_type, parent_id, stage_id):
    # если ad_type равен 1 или 2 (первичное рассмотрение в суде или инспекции), то в parent_id передается pk проверки
    # если ad_type равен 3 (повторное рассмотрение после обжалования), то в parent_id передается pk предыдущего рассмотрения
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    uid = uuid.uuid1().hex
    parent = None
    ad = models.ADRecord()
    ad.doc_type = 'административное дело'
    ad.doc_number = get_next_value('ad')
    ad.doc_date = datetime.now()
    ad.ad_type = ad_type
    ad.inspector = User.objects.get(django_user=request.user)
    if ad_type == 1:
        ad.court_id = 1
    if parent_id != '0':
        parent = Document.objects.get(pk=parent_id)
        ad.parent = parent
        if parent.doc_type == 'административное дело':
            parent.adrecord.has_appeal = True
            parent.adrecord.ad_stage_id = stage_id
            ad.article_id = parent.adrecord.article_id
            parent.adrecord.save()
        ad.organization_id = parent.organization_id
    ad.save()
    if parent:
        ad.houses.set(parent.houses.all())
    form = ADRecordForm(instance=ad)
    context = {'form': form, 'load_static': load_static, 'uid': uid,
               'user_has_perm_to_save': request.user.has_perm('ad.change_adrecord'),
               'document': ad, 'model_name': 'ad_record'}
    return render(request, 'ad/ad_record_form.html', context)


@login_required
@permission_required('ad.change_adrecord', raise_exception=True)
@require_POST
def ad_record_form_save(request):
    ad = models.ADRecord.objects.get(pk=request.POST['pk'])
    form = ADRecordForm(request.POST, instance=ad)
    if form.is_valid():
        form.save()
        return messages.return_success()
    else:
        return messages.return_form_error(form)


@login_required
@permission_required('ad.view_adrecord', raise_exception=True)
def edit_ad_record_form(request, id):
    # если страница открывается самостоятельной вкладкой в браузере, то load_static будет равен True
    # а если она подгружается с помощью jQuery, то load_static будет равен False
    load_static = False if 'HTTP_REFERER' in request.META else True
    uid = uuid.uuid1().hex
    ad = get_object_or_404(models.ADRecord, pk=id)
    form = ADRecordForm(instance=ad)
    context = {'form': form, 'load_static': load_static, 'uid': uid,
               'user_has_perm_to_save': request.user.has_perm('ad.change_adrecord'),
               'document': ad, 'model_name': 'ad_record'}
    return render(request, 'ad/ad_record_form.html', context)


@login_required
@permission_required('ad.view_adrecord', raise_exception=True)
@csrf_exempt
def ad_record_json_table(request):
    return filter.filtered_table_json_response(request, models.ADRecord)


@login_required
@permission_required('ad.view_adrecord', raise_exception=True)
def ad_record_table(request):
    context = {'user_has_perm_to_add': request.user.has_perm('ad.add_adrecord')}
    context.update(csrf(request))
    return render(request, 'ad/ad_record_table.html', context)


@login_required
@permission_required('ad.view_adrecord', raise_exception=True)
@csrf_exempt
def ad_record_list(request):
    pk = request.POST['id']
    model = request.POST['model']
    o = Object(pk, model)
    context = {'ad_records': o.object.document_set.filter(doc_type='административное дело')}
    return render(request, 'ad/ad_record_list.html', context)
