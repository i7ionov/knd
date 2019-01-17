from django import forms

from inspections.models import Inspection


class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ['doc_number', 'doc_date', 'date_begin', 'inspector', 'organization']

    class Media:
        js = ('jquery.min.js', 'jquery.easyui.min.js', 'my.js', 'locale/easyui-lang-ru.js')
        css = {
            'all': ('css/bootstrap.css', 'themes/gray/easyui.css', 'themes/icon.css')
        }

