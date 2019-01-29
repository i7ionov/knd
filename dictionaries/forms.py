from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Organization
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
