from .base import FunctionalTest
from seleniumrequests.request import WebDriverException
import os
import datetime
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10


class InspectionTests(FunctionalTest):
    def test(self):
        self.browser.get(self.live_server_url)
        self.wait_for(lambda: self.assertIn('Вход в систему', self.browser.title))
        self.wait_for(lambda: self.browser.find_element_by_id('_easyui_textbox_input1').send_keys('test_user'))
        self.wait_for(lambda: self.browser.find_element_by_id('_easyui_textbox_input2').send_keys('123'))
        self.wait_for(lambda: self.browser.find_element_by_id('submit').click())

        self.wait_for(lambda: self.assertIn('Учет КНД ИГЖН', self.browser.title))
        self.wait_for(lambda: self.browser.find_element_by_id('inspections_menu').click())
        self.wait_for(lambda: self.browser.find_element_by_id('inspection_table_menu_item').click())
        self.wait_for(lambda: self.browser.find_element_by_id('create_new_insp_button').click())
        # проверка правильности автоматически заполненных полей
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_xpath(
            "//select[contains(@id, 'inspector')]/following::span/input").get_attribute('value'), 'test_user_name'))
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_xpath(
            "//input[contains(@id, 'doc_number')]/following::span/input").get_attribute('value'), '1'))
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_xpath(
            "//input[contains(@id, 'doc_date')]/following::span/input").get_attribute('value'),
                                               datetime.datetime.now().strftime('%d.%m.%Y')))
        # заводим остальные поля
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//input[contains(@id, 'date_begin')]/following::span/input")).send_keys('12.12.2012')
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//input[contains(@id, 'date_begin')]/following::span/input")).send_keys(Keys.RETURN)

        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//select[contains(@id, 'organization')]/following::span/span/a")).click()
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//select[contains(@id, 'organization')]/following::span/input")).send_keys(Keys.DOWN)
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//select[contains(@id, 'organization')]/following::span/input")).send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_xpath(
            "//select[contains(@id, 'organization')]/following::span/input").get_attribute('value'), 'org1, ИНН:123'))

        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//input[contains(@id, 'comment')]")).send_keys('Comm')

        # сохраняем проверку
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//a[contains(@id, 'submit')]")).click()
