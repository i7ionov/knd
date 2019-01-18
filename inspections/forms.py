from django import forms

from inspections.models import Inspection


# http://qaru.site/questions/2090842/how-do-i-pass-a-context-variable-from-a-view-to-a-custom-fieldwidget-in-a-django-template
class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ['doc_number', 'doc_date', 'date_begin', 'inspector', 'organization', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'style': 'width:100%;height:300px'}),
        }

    class Media:
        js = ('jquery.min.js', 'jquery.easyui.min.js', 'my.js', 'locale/easyui-lang-ru.js')
        css = {
            'all': ('css/bootstrap.css', 'themes/gray/easyui.css', 'themes/icon.css')
        }

