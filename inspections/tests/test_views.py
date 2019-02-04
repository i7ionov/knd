from iggndb.tests.base import BaseTest
from django.contrib.auth.models import Permission
from inspections.forms import InspectionForm
from inspections.models import Inspection, ViolationInInspection, ViolationType
from dictionaries.models import Organization, User
import json
from inspections.tests import data
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


class InspectionJsonTableTest(BaseTest):
    def setUp(self):
        super(InspectionJsonTableTest, self).setUp()
        self.insp = Inspection(doc_number='1',
                               doc_date='2011-11-11',
                               date_begin='2011-11-12',
                               date_end='2011-11-13',
                               inspector=self.inspector,
                               )
        self.insp2 = Inspection(doc_number='2',
                                doc_date='2012-11-11',
                                date_begin='2012-11-12',
                                date_end='2012-11-13',
                                inspector=self.inspector,
                                )
        self.insp.save()
        self.insp2.save()
        self.v = ViolationInInspection(violation_type=self.v_type1, count=2, inspection=self.insp)
        self.v.save()

    def test_returns_json(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_inspection'))
        response = self.client.post('/insp/inspection_json_table/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_returns_valid_total_rows_count_with_default_params(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_inspection'))
        data = {'page': ['1'], 'rows': ['20'], 'sort': ['dictionaries_document.id'], 'order': ['desc'],
                'filterRules': ['[]']}
        response = self.client.post('/insp/inspection_json_table/', data=data)
        result = json.loads(response.content.decode('utf8'))
        self.assertEqual(result['total'], 2)

    def test_returns_valid_rows_with_default_params(self):
        pass
        # TODO:

    def test_returns_valid_total_rows_count_with_filters(self):
        pass
        # TODO:


class CreatingInspectionFormTest(BaseTest):

    def test_creating_inspection_uses_template(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        response = self.client.get('/insp/inspection_form/new/0/')
        self.assertTemplateUsed(response, 'inspections/inspection_form.html')

    def test_creating_inspection_uses_form(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        response = self.client.get('/insp/inspection_form/new/0/')
        self.assertIsInstance(response.context['form'], InspectionForm)

    def test_user_can_add_inspection_table_only_with_permission(self):
        response = self.client.get('/insp/inspection_form/new/0/')
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
            'violations': [f'{self.v_type1.pk};undefined', f'{self.v_type2.pk};3'],
            'comment': ['Comm']
        }

    def test_saving_inspection_returns_json(self):
        response = self.client.post('/insp/inspection_form/save/', data=self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_saving_inspection_returns_success(self):
        response = self.client.post('/insp/inspection_form/save/', data=self.data)
        result = json.loads(response.content.decode('utf8'))
        self.assertEqual(result[0]['result'], 'Форма успешно сохранена')

    def test_saved_inspection_equals_initial_data(self):
        self.client.post('/insp/inspection_form/save/', data=self.data)
        insp = Inspection.objects.get(pk=self.data['pk'][0])
        self.assertEqual(self.data['doc_number'][0], insp.doc_number)
        self.assertEqual(self.data['doc_date'][0], insp.doc_date.strftime('%d.%m.%Y'))
        self.assertEqual(self.data['date_begin'][0], insp.date_begin.strftime('%d.%m.%Y'))
        self.assertEqual(self.data['inspector'][0], str(insp.inspector.id))
        self.assertEqual(self.data['organization'][0], str(self.org2.pk))
        self.assertEqual(2, insp.houses.count())
        self.assertEqual(self.data['comment'][0], insp.comment)
        self.assertEqual(insp.violationininspection_set.first().violation_type.id, self.v_type2.id)
        self.assertEqual(insp.violationininspection_set.first().count, 3)
        self.assertEqual(insp.violationininspection_set.count(), 1)


class EditingInspectionFormTest(BaseTest):
    def setUp(self):
        super(EditingInspectionFormTest, self).setUp()
        data.create_inspections()
        self.insp = Inspection.objects.all()[3]

    def test_uses_template(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_inspection'))
        response = self.client.get(f'/insp/inspection_form/{self.insp.pk}/')
        self.assertTemplateUsed(response, 'inspections/inspection_form.html')

    def test_uses_form(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_inspection'))
        response = self.client.get(f'/insp/inspection_form/{self.insp.pk}/')
        self.assertIsInstance(response.context['form'], InspectionForm)

    def test_user_can_edit_inspection_only_with_permission(self):
        response = self.client.get(f'/insp/inspection_form/{self.insp.pk}/')
        self.assertEqual(response.status_code, 403)

    def test_pass_valid_inspection_in_context(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_inspection'))
        response = self.client.get(f'/insp/inspection_form/{self.insp.pk}/')
        self.assertEqual(response.context['document'], self.insp)


class ViolationInInspectionTest(BaseTest):
    def setUp(self):
        super(ViolationInInspectionTest, self).setUp()
        self.user.user_permissions.add(Permission.objects.get(codename='change_inspection'))
        self.insp = Inspection(doc_number='1', doc_date='2011-11-11')
        self.insp.save()
        self.v = ViolationInInspection(violation_type=self.v_type1, count=2, inspection=self.insp)
        self.v.save()

    def test_uses_template(self):
        response = self.client.get(f'/insp/violation_in_inspection_json_list/{self.insp.id}/')
        self.assertTemplateUsed(response, 'inspections/violation_in_inspection_json_list.html')

    def test_contains_violations_info(self):
        response = self.client.get(f'/insp/violation_in_inspection_json_list/{self.insp.id}/')
        self.assertIn('Type of violation', response.content.decode('utf8'))
