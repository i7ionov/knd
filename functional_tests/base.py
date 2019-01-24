from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from seleniumrequests import Firefox
from seleniumrequests.request import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
from django.contrib.auth.models import User as DjangoUser, Permission
from dictionaries.models import Organization, User, Address, House
from inspections.models import Inspection, ViolationInInspection, ViolationType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
from inspections.tests import data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        print(os.path.join(BASE_DIR, 'geckodriver.exe'))
        self.browser = Firefox(executable_path=os.path.join(BASE_DIR, 'geckodriver.exe'))
        self.actionChains = ActionChains(self.browser)
        user = DjangoUser()
        user.username = 'test_user'
        user.set_password('123')
        user.is_staff = True
        user.save()
        User(django_user=user, name='test_user_name').save()
        user.user_permissions.add(Permission.objects.get(codename='view_inspection'))
        user.user_permissions.add(Permission.objects.get(codename='add_inspection'))
        user.user_permissions.add(Permission.objects.get(codename='change_inspection'))
        data.create_inspections()
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

    def select_value(self, element_id):
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            f"//select[contains(@id, '{element_id}')]/following::span/span/a")).click()
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            f"//select[contains(@id, '{element_id}')]/following::span/input")).send_keys(Keys.DOWN)
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            f"//select[contains(@id, '{element_id}')]/following::span/input")).send_keys(Keys.ENTER)

    def add_address(self, house_number):
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//a[contains(@id, 'add_address')]")).click()
        time.sleep(0.5)
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//div[contains(@id, 'address_dialog')]/div/div/div/div/div/table/tbody/tr/td/div")).click()
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//input[contains(@id, 'house_number')]/following::span/input")).send_keys(house_number)
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//a[contains(@id, 'addr_sel_close_btn')]")).click()

    def enter_date(self, element_id, date):
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            f"//input[contains(@id, '{element_id}')]/following::span/input")).click()
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            f"//input[contains(@id, '{element_id}')]/following::span/input")).send_keys(date)
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            f"//input[contains(@id, '{element_id}')]/following::span/input")).send_keys(Keys.ENTER)
