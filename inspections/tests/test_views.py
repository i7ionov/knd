from iggndb.tests.base import BaseTest
from django.contrib.auth.models import Permission
from inspections.forms import InspectionForm


class InspectionTableTest(BaseTest):

    def test_uses_template(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_inspection'))
        response = self.client.get('/insp/inspection_table/')
        self.assertTemplateUsed(response, 'inspections/inspection_table.html')

    def test_user_can_view_inspection_table_only_with_permission(self):
        response = self.client.get('/insp/inspection_table/')
        self.assertEqual(response.status_code, 403)


class InspectionFormTest(BaseTest):

    def test_creating_inspection_uses_template(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        response = self.client.get('/insp/inspection_form/new/')
        self.assertTemplateUsed(response, 'inspections/inspection_form.html')

    def test_creating_inspection_uses_form(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        response = self.client.get('/insp/inspection_form/new/')
        self.assertIsInstance(response.context['form'], InspectionForm)
