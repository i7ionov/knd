"""Модуль содержит методы для выгрузки информации из ГИС ЖКХ"""
from seleniumrequests import Chrome
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import requests, shutil
import zipfile
from iggndb import settings
import os
from datetime import datetime, timedelta
import simplejson as json


class StatusCodeIsNot200Exception(Exception):
    pass


class FileIsNoneException(Exception):
    pass


class UrlIsNoneException(Exception):
    pass


def unpack_zip(file):
    """Метод распаковывает первый файл с расширением xlsx в указанном архиве в папку MEDIA_ROOT/exports
        Возвращает путь к файлу"""
    if file is None:
        raise FileIsNoneException
    if zipfile.is_zipfile(file):
        z = zipfile.ZipFile(file, 'r')
        for filename in z.namelist():
            if filename[-4:] == 'xlsx':
                return z.extract(filename, os.path.join(settings.MEDIA_ROOT, 'exports'))
        z.close()
    return None


def download(url):
    """Метод скачивает файл по ссылке. Сохраняет его по пути MEDIA_ROOT/exports/tempfile.zip.
        В случае успеха возвращает путь к файлу"""
    if url is None:
        raise UrlIsNoneException
    filereq = requests.get(url, stream=True)
    filename = os.path.join(settings.MEDIA_ROOT, 'exports', 'tempfile.zip')
    with open(filename, "wb") as receive:
        shutil.copyfileobj(filereq.raw, receive)
    del filereq
    return filename


def get_file_url(full=False):
    """Метод делает запрос на выгрузку проверок из ГИС ЖКХ.
        После того, как выгрузка будет произведена возвращает ссылку на архив"""
    url = 'https://dom.gosuslugi.ru/'
    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = Chrome(options=options, executable_path='/www/chromedriver', service_log_path='/www/log/chromedriver.log')
    driver.get(url)
    time.sleep(6)
    item = driver.find_element_by_xpath("//div[@class='portal-header__signin fixed roboto ng-scope']/a[1]")
    item.click()
    time.sleep(30)  # секунды
    # заполняем телефон
    tel = driver.find_element_by_class_name("flt_lbl_inp")
    tel.click()
    time.sleep(3)  # секунды
    tel.send_keys('89824782612')
    # пароль
    pas = driver.find_element_by_id("password")
    pas.click()
    time.sleep(3)  # секунды
    pas.send_keys('Ujceckeub')
    # нажимаем кнопку войти
    but = driver.find_element_by_class_name("button-big")
    but.click()
    driver.get_cookies()
    time.sleep(10)  # секунды
    org = driver.find_element_by_id("org0")
    org.click()
    # на этом этапе должно выйти дилоговое окно согласия продолжить работу без использования ГОСТ Р 34.10-2001
    # окно может очень долго открываться
    for i in range(15):
        time.sleep(10)  # секунды
        try:
            item = driver.find_element_by_xpath("//label[1]")
            break
        except NoSuchElementException:
            continue
    item.click()
    item = driver.find_element_by_id("bContinue")
    # на этом этапе происходит нажатие кнопки согласия продолжить работу
    # сервер ГИС ЖКХ может так долго отвечать, что метод click вызовет TimeoutException
    # на него реагировать нет смысла, т.к. вход в ГИС ЖКХ уже в любом случае произведен
    try:
        item.click()
    except TimeoutException:
        pass
    if full:
        date = datetime(2014, 1, 1)
    else:
        date = datetime.now() - timedelta(90)
    # здесь мы делаем запрос на формирование
    response = driver.request('POST', 'https://my.dom.gosuslugi.ru/ext-bus-inspection-ie-service/export/',
                              json={"examinationFrom": date.strftime('%Y-%m-%d'), "operationType": "EXPORT_EXAMINATIONS"})
    # если сервер его не принял, то даже нет смысла дальше продолжать.
    if response.status_code != 200:
        driver.quit()
        raise StatusCodeIsNot200Exception
    print('task sended')
    # тут нужно долго подождать
    timeout = 60
    while timeout > 0:
        time.sleep(1 * 60)  # 2 минуты
        try:
            response = driver.request('POST', 'https://my.dom.gosuslugi.ru/monitoring/api/rest/services/files/search;page=1;itemsPerPage=10',
                                      json={"createDateFrom": '',
                                            "createDateTo": '',
                                            "processDateFrom": '',
                                            "processDateTo": '',
                                            "startProcessingDateFrom": '',
                                            "startProcessingDateTo": ''})

            item = json.loads(response.text)
        except (json.errors.JSONDecodeError, requests.exceptions.ConnectionError):
            timeout = timeout - 1
            continue
        isready = item['items'][0]['downloadAvailable']
        if isready:
            guid = item['items'][0]['resultContentGuid']
            url = 'https://my.dom.gosuslugi.ru/filestore/downloadServlet?uid=' + guid
            break
        else:
            timeout = timeout - 1
            continue
    if url is None:
        raise UrlIsNoneException
    sessionId = driver.get_cookie('sessionId')['value']
    filereq = requests.get(url, stream=True, headers={"Cookie": 'sessionId=' + sessionId})
    filename = os.path.join(settings.MEDIA_ROOT, 'exports', 'tempfile.zip')
    with open(filename, "wb") as receive:
        shutil.copyfileobj(filereq.raw, receive)
    del filereq
    driver.quit()
    return filename


