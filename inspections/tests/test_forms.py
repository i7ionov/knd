from django.test import TestCase
from inspections.forms import InspectionForm


class InspectionFormTest(TestCase):

    def test_form_items_has_css_classes(self):
        form = InspectionForm(prefix='123')
        self.assertIn('class="easyui-textbox"', form.as_p())
