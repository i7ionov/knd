from iggndb.tests.base import BaseTest
from dictionaries.models import House, Address
import json


class AddrFromIDListTest(BaseTest):
    def setUp(self):
        super(AddrFromIDListTest, self).setUp()
        self.addr1 = Address(area='area1', city='city1', place='place1', street='street1')
        self.addr1.save()
        self.house1 = House(number='1', address=self.addr1)
        self.house1.save()
        self.addr2 = Address(area='area2', city='city2', place='place2', street='street2')
        self.addr2.save()
        self.house2 = House(number='2', address=self.addr2)
        self.house2.save()

    def test_addr_from_id_list_returns_json(self):
        data = {'data[]': [self.house1.id, self.house2.id]}
        response = self.client.post('/dict/addr_from_id_list/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_addr_from_id_list_returns_valid_data(self):
        data = {'data[]': [self.house1.id, self.house2.id]}
        response = self.client.post('/dict/addr_from_id_list/', data=data)
        result = json.loads(response.content.decode('utf8'))
        self.assertEqual(result['result'][0][0], str(self.house1.pk))
        self.assertEqual(result['result'][0][1], 'place1, city1, street1, 1')
        self.assertEqual(result['result'][1][0], str(self.house2.pk))
        self.assertEqual(result['result'][1][1], 'place2, city2, street2, 2')


class AddrSelectTest(BaseTest):
    def test_addr_select_returns_html(self):
        data = {'data[]': 'random_uid'}
        response = self.client.post('/dict/addr_select/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dictionaries/address_select.html')

    def test_addr_select_contains_random_uid(self):
        data = {'data[]': 'random_uid'}
        response = self.client.post('/dict/addr_select/', data=data)
        self.assertIn('random_uid', response.content.decode('utf8'))

    def test_addr_select_shields_random_uid(self):
        evil_uid = '<script>alert("Achtung!")</script>'
        data = {'data[]': evil_uid}
        response = self.client.post('/dict/addr_select/', data=data)
        self.assertNotIn(evil_uid, response.content.decode('utf8'))


class AddrTableJSONTest(BaseTest):
    def setUp(self):
        super(AddrTableJSONTest, self).setUp()
        self.addr1 = Address(area='area1', city='city1', place='place1', street='street1')
        self.addr1.save()
        self.house1 = House(number='1', address=self.addr1)
        self.house1.save()
        self.addr2 = Address(area='area2', city='city2', place='place2', street='street2')
        self.addr2.save()
        self.house2 = House(number='2', address=self.addr2)
        self.house2.save()

    def test_addr_table_json_returns_json(self):
        data = {}
        response = self.client.post('/dict/addr_table_json/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_addr_from_id_list_returns_valid_data(self):
        data = {}
        response = self.client.post('/dict/addr_table_json/', data=data)
        result = json.loads(response.content.decode('utf8'))
        self.fail(result)
