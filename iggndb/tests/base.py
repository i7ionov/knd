from django.test import TestCase
from django.urls import resolve
from iggndb.views import index
from django.http import HttpRequest
from django.contrib.auth.models import User as DjangoUser
from dictionaries.models import User
from django.test import Client


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
