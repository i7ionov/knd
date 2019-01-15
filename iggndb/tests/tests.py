from django.test import TestCase
from django.urls import resolve
from iggndb.views import index
from django.http import HttpRequest
from django.contrib.auth.models import User as DjangoUser
from django.test import Client


class MainTest(TestCase):
    def setUp(self):
        user = DjangoUser()
        user.username = 'ivsemionov'
        user.set_password('123')
        user.is_staff = True
        user.save()
        request = HttpRequest
        request.user = user
        self.client = Client()
        self.client.login(username='ivsemionov', password='123')

    def test_index_page(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTemplateUsed(response, 'index.html')



