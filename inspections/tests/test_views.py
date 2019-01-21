from iggndb.tests.base import BaseTest
from django.contrib.auth.models import Permission
from inspections.forms import InspectionForm
from inspections.models import Inspection
from dictionaries.models import Organization, User
import json
from datetime import datetime
from django.db import models


class InspectionTableTest(BaseTest):

    def test_uses_template(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_inspection'))
        response = self.client.get('/insp/inspection_table/')
        self.assertTemplateUsed(response, 'inspections/inspection_table.html')

    def test_user_can_view_inspection_table_only_with_permission(self):
        response = self.client.get('/insp/inspection_table/')
        self.assertEqual(response.status_code, 403)


class CreatingInspectionFormTest(BaseTest):

    def test_creating_inspection_uses_template(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        response = self.client.get('/insp/inspection_form/new/')
        self.assertTemplateUsed(response, 'inspections/inspection_form.html')

    def test_creating_inspection_uses_form(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        response = self.client.get('/insp/inspection_form/new/')
        self.assertIsInstance(response.context['form'], InspectionForm)

    def test_user_can_add_inspection_table_only_with_permission(self):
        response = self.client.get('/insp/inspection_form/new/')
        self.assertEqual(response.status_code, 403)


class SavingInspectionFormTest(BaseTest):
    def setUp(self):
        super(SavingInspectionFormTest, self).setUp()
        self.user.user_permissions.add(Permission.objects.get(codename='change_inspection'))
        insp = Inspection(doc_number='1', doc_date='2011-11-11')
        insp.save()
        self.data = {
            'pk': [insp.pk],
            'doc_number': ['11'],
            'doc_date': ['11.12.2012'],
            'date_begin': ['12.12.2012'],
            'inspector': [str(User.objects.first().pk)],
            'organization': [str(self.org2.pk)],
            'houses': [self.house1.id.__str__(), self.house2.id.__str__()],
            'comment': ['Comm']
        }

    def test_saving_inspection_return_json(self):
        response = self.client.post('/insp/inspection_form/save/', data=self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_saving_inspection_return_success(self):
        response = self.client.post('/insp/inspection_form/save/', data=self.data)
        result = json.loads(response.content.decode('utf8'))
        self.assertEqual(result[0]['result'], 'Форма успешно сохранена')

    def test_saved_inspection_equals_initial_data(self):
        response = self.client.post('/insp/inspection_form/save/', data=self.data)
        insp = Inspection.objects.get(pk=self.data['pk'][0])
        self.assertEqual(self.data['doc_number'][0], insp.doc_number)
        self.assertEqual(self.data['doc_date'][0], insp.doc_date.strftime('%d.%m.%Y'))
        self.assertEqual(self.data['date_begin'][0], insp.date_begin.strftime('%d.%m.%Y'))
        self.assertEqual(self.data['inspector'][0], str(insp.inspector.id))
        self.assertEqual(self.data['organization'][0], str(self.org2.pk))
        self.assertEqual(2, insp.houses.count())
        self.assertEqual(self.data['comment'][0], insp.comment)
