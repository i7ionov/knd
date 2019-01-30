from ad.forms import ADRecordForm
from ad.models import ADRecord
from dictionaries.forms import OrganizationForm
from dictionaries.models import Organization
from iggndb import settings
from inspections.forms import InspectionForm, PreceptForm
from inspections.models import Inspection, Precept


class Object:
    template = None
    form = None
    object = None
    file_location = None
    base_file_url = None

    def __init__(self, pk, model_str):
        if model_str == 'inspection':
            self.object = Inspection.objects.get(id=pk)
            self.form = InspectionForm
            self.template = 'inspections/inspection_form.html'
            self.file_location = f'{settings.MEDIA_ROOT}/inspection/{self.object.doc_number}{self.object.doc_date}'
            self.base_file_url = f'/media/inspection/{self.object.doc_number}{self.object.doc_date}'
        elif model_str == 'precept':
            self.object = Precept.objects.get(id=pk)
            self.form = PreceptForm
            self.template = 'inspections/precept_form.html'
            self.file_location = f'{settings.MEDIA_ROOT}/precept/{self.object.doc_number}{self.object.doc_date}'
            self.base_file_url = f'/media/precept/{self.object.doc_number}{self.object.doc_date}'
        elif model_str == 'ad_record':
            self.object = ADRecord.objects.get(id=pk)
            self.form = ADRecordForm
            self.template = 'ad/ad_record_form.html'
            self.file_location = f'{settings.MEDIA_ROOT}/ad_record/{self.object.doc_number}{self.object.doc_date}'
            self.base_file_url = f'/media/ad_record/{self.object.doc_number}{self.object.doc_date}'
        elif model_str == 'organization':
            self.object = Organization.objects.get(id=pk)
            self.form = OrganizationForm
            self.template = 'dictionaries/org_form.html'
            self.file_location = f'{settings.MEDIA_ROOT}/organization/{self.object.pk}'
            self.base_file_url = f'/media/organization/{self.object.pk}'




