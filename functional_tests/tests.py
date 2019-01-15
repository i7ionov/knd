from .base import FunctionalTest
from seleniumrequests.request import WebDriverException
import os
import time
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
        self.wait_for(lambda: self.browser.find_element_by_id('doc_number').click())


