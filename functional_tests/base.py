from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from seleniumrequests import Firefox
from seleniumrequests.request import WebDriverException
from django.contrib.auth.models import User as DjangoUser, Permission
from dictionaries.models import Organization, User, Address, House
from inspections.models import Inspection, ViolationInInspection, ViolationType
import os
import time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        print(os.path.join(BASE_DIR, 'geckodriver.exe'))
        self.browser = Firefox(executable_path=os.path.join(BASE_DIR, 'geckodriver.exe'))
        user = DjangoUser()
        user.username = 'test_user'
        user.set_password('123')
        user.is_staff = True
        user.save()
        User(django_user=user, name='test_user_name').save()
        user.user_permissions.add(Permission.objects.get(codename='view_inspection'))
        user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        user.user_permissions.add(Permission.objects.get(codename='change_inspection'))

        org = Organization(name='org1', inn='123')
        org.save()
        addr1 = Address(area='area1', city='city1', place='place1', street='street1')
        addr1.save()
        addr2 = Address(area='area2', city='city2', place='place2', street='street2')
        addr2.save()
        v_type1 = ViolationType(text='Type of violation1')
        v_type1.save()
        v_type2 = ViolationType(text='Type of violation2')
        v_type2.save()
        v_type2 = ViolationType(text='Type of violation22', parent=v_type2)
        v_type2.save()

    def tearDown(self):
        pass
        # self.browser.quit()

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)



