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
        self.enter_date('date_begin', datetime.datetime.now().strftime('%d.%m.%Y'))
        self.enter_date('date_end', datetime.datetime.now().strftime('%d.%m.%Y'))
        self.enter_date('act_date', datetime.datetime.now().strftime('%d.%m.%Y'))
        self.select_value('organization')
        self.select_value('legal_basis')
        self.select_value('control_kind')
        self.select_value('control_form')
        self.select_value('control_plan')
        self.select_value('inspection_result')
        self.select_value('cancellation')
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//textarea[contains(@id, 'comment')]/following::span/textarea")).send_keys('Comm')

        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//tr[contains(@class, 'datagrid-row')]/td/div/span[contains(text(),'Type of violation22')]")).click()
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//input[@class='datagrid-editable-input numberbox-f textbox-f']/following::span/input")).send_keys('123')

        self.add_address('1б')
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//div[contains(@id, 'addresses')]/div/div/div/div/div/table/tbody/tr/td/div")).click()
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//a[contains(@id, 'remove_address')]")).click()
        self.add_address('1а')

        self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//a[contains(@id, 'submit')]")).click()

        self.wait_for(lambda: self.browser.find_element_by_class_name('tabs-close')).click()
        self.wait_for(lambda: self.browser.find_element_by_class_name('tabs-close')).click()

        self.wait_for(lambda: self.browser.find_element_by_id('inspections_menu').click())
        self.wait_for(lambda: self.browser.find_element_by_id('inspection_table_menu_item').click())

        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_xpath(
            "//tr[contains(@class, 'datagrid-row')]/td[2]").text, '1'))

        self.actionChains.double_click(self.wait_for(lambda: self.browser.find_element_by_xpath(
            "//tr[contains(@class, 'datagrid-row')]/td[2]"))).perform()





