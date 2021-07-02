from django import forms
from django.utils.translation import gettext_lazy as _

from dictionaries.widgets.organization import OrganizationWidget
from .models import Organization, House, Address
from iggn_tools.widgets.none_widget import NoneWidget


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'inn', 'ogrn', 'is_bankrupt', 'kpp', 'org_type', 'location_address',
                  'telephone', 'email', 'comment']
        widgets = {
            'comment': NoneWidget(),
        }
        labels = {
            'comment': _(''),
        }

    class Media:
        js = ('jquery.min.js', 'jquery.easyui.min.js', 'my.js')
        css = {
            'all': ('css/bootstrap.css', 'themes/gray/easyui.css', 'themes/icon.css')
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['area', 'place', 'city', 'street']

    class Media:
        js = ('jquery.min.js', 'jquery.easyui.min.js', 'my.js')
        css = {
            'all': ('css/bootstrap.css', 'themes/gray/easyui.css', 'themes/icon.css')
        }



class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['number', 'organization', 'comment', 'building_year', 'number_of_apartments', 'total_area',
                  'living_area',
                  'non_living_area', 'changing_doc_number', 'changing_doc_date', 'changing_doc_header',
                  'changing_org_date', 'agr_conclusion_date', 'management_start_date',
                  'exclusion_date', 'exclusion_legal_basis']
        widgets = {
            'comment': NoneWidget(),
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
