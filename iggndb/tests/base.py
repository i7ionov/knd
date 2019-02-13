from datetime import timedelta, datetime

from django.test import TestCase
from django.urls import resolve
from iggndb.views import index
from django.http import HttpRequest
from django.contrib.auth.models import User as DjangoUser
from dictionaries.models import User, Organization, Address, House, Department, OrganizationType
from django.test import Client
from inspections.models import Inspection, ViolationInInspection, ViolationType, ControlKind, PreceptResult, \
    ControlForm, LegalBasis, InspectionResult, ControlPlan


class BaseTest(TestCase):
    user = None
    request = None

    def setUp(self):
        self.user = DjangoUser()
        self.user.username = 'ivsemionov'
        self.user.set_password('123')
        self.user.is_staff = True
        self.user.save()
        self.user2 = DjangoUser()
        self.user2.username = 'user2'
        self.user2.set_password('123')
        self.user2.is_staff = False
        self.user2.save()
        self.request = HttpRequest
        self.request.user = self.user
        self.client = Client()
        self.client.login(username='ivsemionov', password='123')
        self.dep1 = Department(name='Dep1')
        self.dep1.save()
        self.dep2 = Department(name='Dep2')
        self.dep2.save()
        self.inspector1 = User(name='user1', department=self.dep1, django_user=self.user)
        self.inspector1.save()
        self.inspector2 = User(name='user2', department=self.dep2, django_user=self.user2)
        self.inspector2.save()
        self.org_type_ul = OrganizationType(text="Юридическое лицо")
        self.org_type_ul.save()
        self.org_type_fl = OrganizationType(text="Физическое лицо")
        self.org_type_fl.save()
        self.org_type_mo = OrganizationType(text="Орган местного самоуправления")
        self.org_type_mo.save()
        self.org1 = Organization(name='org1', inn='123', org_type=self.org_type_ul)
        self.org1.save()
        self.org2 = Organization(name='org2', inn='222', org_type=self.org_type_ul)
        self.org2.save()
        self.org3 = Organization(name='org3', inn='2232', org_type=self.org_type_fl)
        self.org3.save()
        self.org4 = Organization(name='org4', inn='2224', org_type=self.org_type_mo)
        self.org4.save()
        self.addr1 = Address(area='area1', city='city1', place='place1', street='street1')
        self.addr1.save()
        self.house1 = House(number='1', address=self.addr1, total_area=123)
        self.house1.save()
        self.house3 = House(number='3', address=self.addr1, total_area=100)
        self.house3.save()
        self.addr2 = Address(area='area2', city='city2', place='place2', street='street2')
        self.addr2.save()
        self.house2 = House(number='2', address=self.addr2, total_area=321)
        self.house2.save()
        self.v_type1 = ViolationType(text='Type of violation1')
        self.v_type1.save()
        self.v_type2 = ViolationType(text='Type of violation2')
        self.v_type2.save()
        self.v_type3 = ViolationType(text='Type of violation3')
        self.v_type3.save()
        self.control_kind_gn = ControlKind(text='Жилищный надзор', pk=1)
        self.control_kind_gn.save()
        self.control_kind_lk = ControlKind(text='Лиензионный контроль', pk=2)
        self.control_kind_lk.save()
        self.control_form_doc = ControlForm(text='Документарная')
        self.control_form_doc.save()
        self.control_form_out = ControlForm(text='Выездная')
        self.control_form_out.save()
        self.control_form_doc_out = ControlForm(text='Выездная и документарная')
        self.control_form_doc_out.save()
        self.control_form_other = ControlForm(text='Другое')
        self.control_form_other.save()
        self.control_plan = ControlPlan(text='Плановая', pk=1)
        self.control_plan.save()
        self.control_vneplan = ControlPlan(text='Внелановая', pk=2)
        self.control_vneplan.save()
        self.legal_basis1 = LegalBasis(text='Поступление обращений и заявлений граждан')
        self.legal_basis1.save()
        self.legal_basis2 = LegalBasis(
            text='Приказ (распоряжение) руководителяна основании требования прокурора')
        self.legal_basis2.save()
        self.legal_basis3 = LegalBasis(
            text='Проверка предписания')
        self.legal_basis3.save()
        self.inspection_result_test = InspectionResult(text='Тестовая проверка')
        self.inspection_result_test.save()
        self.inspection_result1 = InspectionResult(text='Проверка проведена, составлен акт проверки')
        self.inspection_result1.save()
        self.inspection_result2 = InspectionResult(
            text='Составлен акт о невозможности проведения проверки (документы не представлены частично)')
        self.inspection_result2.save()
        self.inspection_result3 = InspectionResult(
            text='документы не представлены полностью')
        self.inspection_result3.save()
        self.inspection_result4 = InspectionResult(text='Ликвидация проверяемой организации')
        self.inspection_result4.save()
        self.inspection_result5 = InspectionResult(text='Проверка предписания')
        self.inspection_result5.save()

        self.now = datetime.today()
        td = timedelta(35)
        self.month_ago = self.now - td
        self.month_later = self.now + td
        self.insp1 = Inspection(doc_number='1',
                                doc_date=self.now,
                                organization=self.org1,
                                control_plan=self.control_vneplan,
                                inspector=self.inspector1,
                                control_form=self.control_form_doc,
                                control_kind=self.control_kind_gn,
                                legal_basis=self.legal_basis1,
                                inspection_result=self.inspection_result1)
        self.insp1.save()
        self.insp1.houses.add(self.house1)
        self.violation1 = ViolationInInspection(violation_type=self.v_type1, count=2, inspection=self.insp1)
        self.violation1.save()

        self.insp2 = Inspection(doc_number='2',
                                doc_date=self.now,
                                inspector=self.inspector1,
                                organization=self.org1,
                                control_plan=self.control_plan,
                                control_form=self.control_form_doc,
                                control_kind=self.control_kind_gn,
                                legal_basis=self.legal_basis1,
                                inspection_result=self.inspection_result1)
        self.insp2.save()
        self.insp2.houses.add(self.house2)
        self.violation2 = ViolationInInspection(violation_type=self.v_type2, count=3, inspection=self.insp1)
        self.violation2.save()

        self.insp3 = Inspection(doc_number='2',
                                doc_date=self.now,
                                inspector=self.inspector2,
                                organization=self.org2,
                                control_form=self.control_form_doc,
                                control_kind=self.control_kind_gn,
                                legal_basis=self.legal_basis1,
                                inspection_result=self.inspection_result1)
        self.insp3.save()
        self.insp3.houses.add(self.house3)
        self.violation3 = ViolationInInspection(violation_type=self.v_type2, count=3, inspection=self.insp1)
        self.violation3.save()

