from django import forms
from django.utils.translation import gettext_lazy as _
from ad.models import ADRecord
from dictionaries.widgets.address_list import AddressListWidget
from iggn_tools.widgets.none_widget import NoneWidget


# http://qaru.site/questions/2090842/how-do-i-pass-a-context-variable-from-a-view-to-a-custom-fieldwidget-in-a-django-template
class ADRecordForm(forms.ModelForm):
    class Meta:
        model = ADRecord
        fields = ['ad_stage', 'article', 'organization', 'protocol_date', 'referring_to_instance_date',
                  'court', 'adjudication', 'adjudication_amount_of_fine', 'adjudication_date', 'adjudication_start_date',
                  'date_of_receipt_unlegal', 'date_of_receipt_legal', 'publish_gisgkh_date',
                  'publish_erp_date', 'box_number', 'comment', 'houses']
        widgets = {
            'comment': NoneWidget(),
            'houses': AddressListWidget(),
        }
        labels = {
            'comment': _(''),
        }

    class Media:
        js = ('jquery.min.js', 'jquery.easyui.min.js', 'my.js')
        css = {
            'all': ('css/bootstrap.css', 'themes/gray/easyui.css', 'themes/icon.css')
        }
