from django.test import TestCase
from dictionaries.widgets.address_list import AddressListWidget
from iggndb.tests.base import BaseTest
from dictionaries.models import House, Address
import json


class AddressListTest(TestCase):
    def setUp(self):
        super(AddressListTest, self).setUp()
        self.addr1 = Address(area='area1', city='city1', place='place1', street='street1')
        self.addr1.save()
        self.house1 = House(number='1', address=self.addr1)
        self.house1.save()
        self.addr2 = Address(area='area2', city='city2', place='place2', street='street2')
        self.addr2.save()
        self.house2 = House(number='2', address=self.addr2)
        self.house2.save()

    def test_address_list_contains_easyui_datalist(self):
        widget = AddressListWidget()
        self.assertIn('easyui-datalist', widget.render('name', [1]))

