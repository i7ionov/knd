from iggndb.tests.base import BaseTest
from django.contrib.auth.models import Permission
from inspections.forms import InspectionForm
from inspections.models import Inspection, ViolationInInspection, ViolationType, Precept
from dictionaries.models import Organization, User, Document
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

    def test_response_pass_user_rights_in_context(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_inspection'))
        response = self.client.get('/insp/inspection_table/')
        self.assertEqual(response.context['user_has_perm_to_add'], True)


class InspectionListTest(BaseTest):
    def test_uses_template(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_inspection'))
        data = {'id': [self.org1.pk], 'model': ['organization']}
        response = self.client.post('/insp/inspection_list/', data)
        self.assertTemplateUsed(response, 'inspections/inspection_list.html')

    def test_user_can_view_inspection_list_only_with_permission(self):
        data = {'id': [self.org1.pk], 'model': ['organization']}
        response = self.client.post('/insp/inspection_list/', data)
        self.assertEqual(response.status_code, 403)

    def test_response_pass_inspections_in_context(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_inspection'))
        data = {'id': [self.org1.pk], 'model': ['organization']}
        response = self.client.post('/insp/inspection_list/', data)
        self.assertIn(Document.objects.get(pk=self.insp.pk), list(response.context['inspections']))
        self.assertIn(Document.objects.get(pk=self.insp2.pk), list(response.context['inspections']))
        self.assertNotIn(Document.objects.get(pk=self.insp3.pk), list(response.context['inspections']))


class PreceptListTest(BaseTest):
    def setUp(self):
        super(PreceptListTest, self).setUp()
        self.precept = Precept(doc_number='1',
                               doc_type='предписание',
                               doc_date='2011-11-11',
                               organization=self.org1,
                               )
        self.precept2 = Precept(doc_number='2',
                                doc_type='предписание',
                                doc_date='2012-11-11',
                                organization=self.org1,
                                )
        self.precept3 = Precept(doc_number='3',
                                doc_type='предписание',
                                doc_date='2012-11-11',
                                organization=self.org2,
                                )
        self.precept.save()
        self.precept2.save()
        self.precept3.save()

    def test_uses_template(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_precept'))
        data = {'id': [self.org1.pk], 'model': ['organization']}
        response = self.client.post('/insp/precept_list/', data)
        self.assertTemplateUsed(response, 'inspections/precept_list.html')

    def test_user_can_view_precept_list_only_with_permission(self):
        data = {'id': [self.org1.pk], 'model': ['organization']}
        response = self.client.post('/insp/precept_list/', data)
        self.assertEqual(response.status_code, 403)

    def test_response_pass_precepts_in_context(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_precept'))
        data = {'id': [self.org1.pk], 'model': ['organization']}
        response = self.client.post('/insp/precept_list/', data)
        self.assertIn(Document.objects.get(pk=self.precept.pk), list(response.context['precepts']))
        self.assertIn(Document.objects.get(pk=self.precept2.pk), list(response.context['precepts']))
        self.assertNotIn(Document.objects.get(pk=self.precept3.pk), list(response.context['precepts']))


class CreatingInspectionFormTest(BaseTest):
    def test_uses_template(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        response = self.client.get(f'/insp/inspection_form/new/{self.control_kind_gn.pk}/')
        self.assertTemplateUsed(response, 'inspections/inspection_form.html')

    def test_uses_form(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        response = self.client.get(f'/insp/inspection_form/new/{self.control_kind_gn.pk}/')
        self.assertIsInstance(response.context['form'], InspectionForm)

    def test_user_can_add_inspection_only_with_permission(self):
        response = self.client.get(f'/insp/inspection_form/new/{self.control_kind_gn.pk}/')
        self.assertEqual(response.status_code, 403)

    def test_response_pass_uid_in_context(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        response = self.client.get(f'/insp/inspection_form/new/{self.control_kind_gn.pk}/')
        self.assertIn('uid', response.context)

    def test_response_pass_user_rights_in_context(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_inspection'))
        response = self.client.get(f'/insp/inspection_form/new/{self.control_kind_gn.pk}/')
        self.assertEqual(response.context['user_has_perm_to_save'], True)

    def test_response_pass_user_rights_in_context2(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        response = self.client.get(f'/insp/inspection_form/new/{self.control_kind_gn.pk}/')
        self.assertEqual(response.context['user_has_perm_to_save'], False)

    def test_response_pass_inspection_in_context(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        response = self.client.get(f'/insp/inspection_form/new/{self.control_kind_gn.pk}/')
        self.assertIsInstance(response.context['document'], Inspection)
        self.assertEqual(response.context['document'].doc_type, 'проверка')

    def test_inspection_has_valid_control_kind(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        response = self.client.get(f'/insp/inspection_form/new/{self.control_kind_gn.pk}/')
        self.assertEqual(response.context['document'].control_kind, self.control_kind_gn)
        response = self.client.get(f'/insp/inspection_form/new/{self.control_kind_lk.pk}/')
        self.assertEqual(response.context['document'].control_kind, self.control_kind_lk)

    def test_inspection_doc_number_has_postfix(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        # если лицензионный контроль, то в номере документа должна быть л
        response = self.client.get(f'/insp/inspection_form/new/{self.control_kind_lk.pk}/')
        self.assertIn('л', response.context['document'].doc_number)
        # если жилищный надзор, то это должна быть просто цифра
        response = self.client.get(f'/insp/inspection_form/new/{self.control_kind_gn.pk}/')
        self.assertIsInstance(response.context['document'].doc_number, int)

    def test_response_pass_model_name_in_context(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        response = self.client.get(f'/insp/inspection_form/new/{self.control_kind_gn.pk}/')
        self.assertEqual(response.context['model_name'], 'inspection')


class RepeatingInspectionFormTest(BaseTest):
    def setUp(self):
        super(RepeatingInspectionFormTest, self).setUp()
        self.precept = Precept(doc_number='1',
                               doc_type='предписание',
                               doc_date='2011-11-11',
                               organization=self.org1,
                               parent=self.insp
                               )
        self.precept.save()
        self.precept.houses.add(self.house1)

    def test_response_pass_valid_inspection(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        response = self.client.get(f'/insp/inspection_form/repeat/{self.precept.pk}/')
        self.assertEqual(response.context['document'].doc_number, '1/1')
        self.assertEqual(response.context['document'].doc_date.date(), data.datetime.now().date())
        self.assertEqual(response.context['document'].organization, self.precept.organization)
        self.assertIn(self.house1, list(response.context['document'].houses.all()))
        self.assertEqual(response.context['document'].parent, self.precept)


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