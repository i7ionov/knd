from django.test import TestCase
from django.urls import resolve
from iggndb.views import index
from django.http import HttpRequest
from django.contrib.auth.models import User as DjangoUser
from dictionaries.models import User, Organization, Address, House
from django.test import Client
from inspections.models import Inspection, ViolationInInspection, ViolationType, ControlKind, PreceptResult, \
    ControlForm, LegalBasis, InspectionResult


class BaseTest(TestCase):
    user = None
    request = None

    def setUp(self):
        self.org1 = Organization(name='org1', inn='123')
        self.org1.save()
        self.org2 = Organization(name='org2', inn='222')
        self.org2.save()
        self.org3 = Organization(name='org3', inn='2232')
        self.org3.save()
        self.org4 = Organization(name='org4', inn='2224')
        self.org4.save()
        self.addr1 = Address(area='area1', city='city1', place='place1', street='street1')
        self.addr1.save()
        self.house1 = House(number='1', address=self.addr1)
        self.house1.save()
        self.addr2 = Address(area='area2', city='city2', place='place2', street='street2')
        self.addr2.save()
        self.house2 = House(number='2', address=self.addr2)
        self.house2.save()
        self.v_type1 = ViolationType(text='Type of violation1')
        self.v_type1.save()
        self.v_type2 = ViolationType(text='Type of violation2')
        self.v_type2.save()
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

