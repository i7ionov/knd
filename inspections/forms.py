from django import forms

from inspections.models import Inspection
from dictionaries.widgets.address_list import AddressListWidget


# http://qaru.site/questions/2090842/how-do-i-pass-a-context-variable-from-a-view-to-a-custom-fieldwidget-in-a-django-template
class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ['doc_number', 'doc_date', 'date_begin', 'inspector', 'organization', 'comment', 'houses']
        widgets = {
            'comment': forms.Textarea(attrs={'style': 'width:100%;height:300px'}),
            'houses': AddressListWidget(),
        }

    class Media:
        js = ('jquery.min.js', 'jquery.easyui.min.js')
        css = {
            'all': ('css/bootstrap.css', 'themes/gray/easyui.css', 'themes/icon.css')
        }

