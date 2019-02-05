from django.test import TestCase
from django.urls import resolve
from iggndb.views import index
from django.http import HttpRequest
from django.contrib.auth.models import User as DjangoUser
from dictionaries.models import User, Organization, Address, House
from django.test import Client
from inspections.models import Inspection, ViolationInInspection, ViolationType, ControlKind, PreceptResult


class BaseTest(TestCase):
    user = None
    request = None

    def setUp(self):
        self.user = DjangoUser()
        self.user.username = 'ivsemionov'
        self.user.set_password('123')
        self.user.is_staff = True
        self.user.save()
        self.inspector = User(django_user=self.user)
        self.inspector.save()
        self.request = HttpRequest
        self.request.user = self.user
        self.client = Client()
        self.client.login(username='ivsemionov', password='123')
        self.org1 = Organization(name='org1', inn='123')
        self.org1.save()
        self.org2 = Organization(name='org2', inn='222')
        self.org2.save()
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

