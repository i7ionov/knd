from iggndb.tests.base import BaseTest
from dictionaries.models import House, Address
import json
from django.contrib.auth.models import Permission


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
        data = {'uid': 'random_uid', 'name': 'random_name'}
        response = self.client.post('/dict/addr_select/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dictionaries/address_select.html')

    def test_addr_select_contains_random_uid(self):
        data = {'uid': 'random_uid', 'name': 'random_name'}
        response = self.client.post('/dict/addr_select/', data=data)
        self.assertIn('random_uid', response.content.decode('utf8'))

    def test_addr_select_shields_random_uid(self):
        evil_string = '<script>alert("Achtung!")</script>'
        data = {'uid': evil_string, 'name': evil_string}
        response = self.client.post('/dict/addr_select/', data=data)
        self.assertNotIn(evil_string, response.content.decode('utf8'))


class AddrTableJSONTest(BaseTest):

    def test_addr_table_json_returns_json(self):
        data = {}
        response = self.client.post('/dict/addr_table_json/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_addr_from_id_list_returns_valid_data(self):
        data = {}
        response = self.client.post('/dict/addr_table_json/', data=data)
        result = json.loads(response.content.decode('utf8'))
        valid_json = {'total': 2, 'rows': [
            {'id': self.addr1.id, 'area': self.addr1.area.__str__(), 'place': self.addr1.place.__str__(), 'city': self.addr1.city.__str__(),
             'city_weight': self.addr1.city_weight.__str__(), 'street': self.addr1.street.__str__()},
            {'id': self.addr2.id, 'area': self.addr2.area.__str__(), 'place': self.addr2.place.__str__(), 'city': self.addr2.city.__str__(),
             'city_weight': self.addr2.city_weight.__str__(), 'street': self.addr2.street.__str__()}]}
        self.assertEqual(result['total'], 2)
        self.assertEqual(valid_json, result)


class AddrTableTest(BaseTest):
    def test_addr_select_returns_html(self):
        response = self.client.get('/dict/addr_table/?uid=random_uid')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dictionaries/address_table.html')


class GetHouseIdTest(BaseTest):
    def setUp(self):
        super(GetHouseIdTest, self).setUp()
        self.addr1 = Address(area='area1', city='city1', place='place1', street='street1')
        self.addr1.save()

    def test_get_house_id_returns_html(self):
        data = {'addr_id': self.addr1.id, 'house_number': '1a'}
        response = self.client.post('/dict/get_house_id/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_house_id_create_correct_record(self):
        data = {'addr_id': self.addr1.id, 'house_number': '1a'}
        response = self.client.post('/dict/get_house_id/', data=data)
        result = json.loads(response.content.decode('utf8'))
        created_house_record = House.objects.get(pk=result['result'])
        self.assertEqual(created_house_record.number, '1a')
        self.assertEqual(created_house_record.address.id, self.addr1.id)

    def test_get_house_id_returns_existing_record(self):
        data = {'addr_id': self.addr1.id, 'house_number': '1??'}
        house = House(address=self.addr1, number='1??')
        house.save()
        response = self.client.post('/dict/get_house_id/', data=data)
        result = json.loads(response.content.decode('utf8'))
        self.assertEqual(house.id, result['result'])

    def test_get_house_id_removes_spaces_and_slashes(self):
        data = {'addr_id': self.addr1.id, 'house_number': '1??'}
        response = self.client.post('/dict/get_house_id/', data=data)
        id1 = json.loads(response.content.decode('utf8'))['result']
        data = {'addr_id': self.addr1.id, 'house_number': '1/??'}
        response = self.client.post('/dict/get_house_id/', data=data)
        id2 = json.loads(response.content.decode('utf8'))['result']
        data = {'addr_id': self.addr1.id, 'house_number': '1  ??'}
        response = self.client.post('/dict/get_house_id/', data=data)
        id3 = json.loads(response.content.decode('utf8'))['result']
        self.assertEqual(id1, id2)
        self.assertEqual(id2, id3)


