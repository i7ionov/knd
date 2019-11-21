from django import forms
from django.utils.translation import gettext_lazy as _
from inspections.models import Inspection, Precept
from dictionaries.widgets.address_list import AddressListWidget
from dictionaries.widgets.organization import OrganizationWidget
from iggn_tools.widgets.none_widget import NoneWidget


# http://qaru.site/questions/2090842/how-do-i-pass-a-context-variable-from-a-view-to-a-custom-fieldwidget-in-a-django-template
class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ['doc_number', 'doc_date', 'date_begin', 'date_end', 'legal_basis', 'control_kind', 'control_form',
                  'control_plan', 'inspection_tasks', 'inspector', 'organization', 'comment', 'houses', 'inspection_result', 'cancellation',
                  'act_date', 'no_preception_needed', 'RPN_notification']
        widgets = {
            'comment': NoneWidget(),
            'houses': AddressListWidget(),
            'organization': OrganizationWidget(),
        }
        labels = {
            'comment': _(''),
        }

    class Media:
        js = ('jquery.min.js', 'jquery.easyui.min.js', 'my.js')
        css = {
            'all': ('css/bootstrap.css', 'themes/gray/easyui.css', 'themes/icon.css')
        }


class PreceptForm(forms.ModelForm):
    class Meta:
        model = Precept
        fields = ['doc_number', 'doc_date', 'precept_begin_date', 'precept_end_date', 'precept_result', 'recalculation',
                  'prolongation_date', 'organization', 'houses',
                  'comment']
        widgets = {
            'comment': NoneWidget(),
            'houses': AddressListWidget(),
            'organization': OrganizationWidget(),
        }
        labels = {
            'comment': _(''),
        }

    class Media:
        js = ('jquery.min.js', 'jquery.easyui.min.js', 'my.js')
        css = {
            'all': ('css/bootstrap.css', 'themes/gray/easyui.css', 'themes/icon.css')
        }
