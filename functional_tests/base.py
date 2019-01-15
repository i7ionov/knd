from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from seleniumrequests import Firefox
from seleniumrequests.request import WebDriverException
from django.contrib.auth.models import User as DjangoUser
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

    def tearDown(self):
        pass
        self.browser.quit()

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
