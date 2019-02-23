# -*- coding: utf-8 -*-
import uuid

from dictionaries.tools import normalize_house_number
from iggn_tools import filter
import xlrd, openpyxl
import django
from django.core.files.base import ContentFile
from openpyxl.writer.excel import save_virtual_workbook

import inspections.models
import dictionaries.models
import analytic.models
from django.core.exceptions import MultipleObjectsReturned
from datetime import datetime
from django.utils import timezone


def import_insp_from_gis_gkh(file):
    rb = xlrd.open_workbook(file)
    sheet = rb.sheet_by_index(0)
    row = 2
    while row < sheet.nrows and sheet.row_values(row)[0] != '':
        val = sheet.row_values(row)
        if val[4] == '':
            print("Пропущена запись №" + str(val[0]))
            row = row + 1
            continue
        number = val[4].replace('Распоряжение № ', '')
        insp, created = inspections.models.Inspection.objects.get_or_create(doc_number=number, doc_date=datetime.strptime(val[5], '%d.%m.%Y').date())
        insp.gis_gkh_number = val[1]
        insp.erp_number = val[3]
        insp.doc_type = "проверка"
        insp.control_form = inspections.models.ControlForm.objects.get(text=val[8])
        insp.control_plan = inspections.models.ControlPlan.objects.get(text=val[6])
        if val[7] == "Государственный и муниципальный жилищный надзор (контроль)":
            insp.control_kind = inspections.models.ControlKind.objects.get(pk=1)
        elif val[7] == "Лицензионный контроль":
            insp.control_kind = inspections.models.ControlKind.objects.get(pk=2)
        # если не введен ОГРН, то это, скорее всего гражданин
        # или если ОГРН введен, но у нас такого нет
        if val[13] != "" and dictionaries.models.Organization.objects.filter(ogrn=val[13]).count() == 0:
            # ищем или создаем по названию
            try:
                org, created = dictionaries.models.Organization.objects.get_or_create(name=val[12])
                if created:
                    org.name = val[12]
                    org.inn = "ОГРН: " + val[13]
                    org.ogrn = val[13]
                    org.kpp = val[14]
                    if val[11] == 'Организация':
                        org.org_type_id = 2
                    else:
                        org.org_type_id = 3
                    org.save()
                insp.organization = org
            except MultipleObjectsReturned:
                print("Несколько организаций с именем " + val[12])
        # если у нас эта организация уже есть
        elif dictionaries.models.Organization.objects.filter(ogrn=val[13]).count() == 1 and val[11] != 'Гражданин':
            # находим ее по огрн
            org = dictionaries.models.Organization.objects.get(ogrn=val[13])
            insp.organization = org
        # если это гражданин
        else:
            # ищем или создаем по названию
            try:
                org, created = dictionaries.models.Organization.objects.get_or_create(name=val[12])
                if created:
                    org.name = val[12]
                    org.inn = val[12]
                    org.ogrn = val[12]
                    org.org_type_id = 1
                    org.save()
                insp.organization = org
            except MultipleObjectsReturned:
                print("Несколько организаций с именем " + val[12])

        try:
            if val[16] != '':
                insp.legal_basis, created = inspections.models.LegalBasis.objects.get_or_create(text=val[16])
        except: print("Не удалость сохранить основание для №" + str(val[0]))

        if val[17] != '':
            insp.date_begin = datetime.strptime(val[17], '%d.%m.%Y').date()
        if val[18] != '':
            insp.date_end = datetime.strptime(val[18], '%d.%m.%Y').date()
        if val[28] != '':
            insp.act_date = datetime.strptime(val[17], '%d.%m.%Y').date()
            if insp.inspection_result is None:
                insp.inspection_result_id = 1
        insp.save()
        row = row + 1


def import_addr_from_gis_gkh(file):
    rb = xlrd.open_workbook(file)
    sheet = rb.sheet_by_index(1)
    row = 2
    while row < sheet.nrows and sheet.row_values(row)[0] != '':
        val = sheet.row_values(row)
        if val[2] == '':
            print("Пропущена запись №" + str(val[0]))
            row = row + 1
            continue
        street = val[7].replace('пр-кт.', 'пр-кт')\
            .replace('б-р.', 'б-р')\
            .replace('проезд.', 'проезд')\
            .replace('тракт.', 'тракт') \
            .replace('ул. Барамзиной', 'ул. Барамзиной Татьяны') \
            .replace('ул. Алексея Кирьянова', 'ул. Кирьянова') \
            .replace('наб. Ириловская', 'Ириловская набережная') \
            .replace('наб. Иренская', 'Иренская набережная') \
            .replace('тракт Ленский', 'Ленский тракт') \
            .replace('л. Им газ. Правда', 'ул. им. газ. Правда')
        if val[5] != '':
            try:
                city = val[5].replace('п. ', '')
                addr = dictionaries.models.Address.objects.get(city=city, street=street)
                house, created = dictionaries.models.House.objects.get_or_create(address=addr, number=val[8])
                insp = inspections.models.Inspection.objects.get(gis_gkh_number=val[1])
                insp.houses.add(house)
                insp.save()
            except dictionaries.models.Address.DoesNotExist:
                print("Не найдена запись: " + val[5] + val[7])
            except inspections.models.Inspection.DoesNotExist:
                print("Не найдена проверка: " + val[1])
            except MultipleObjectsReturned:
                print("Несколько адресов " + val[5] + val[7])
        else:
            try:
                city = val[6].replace('п. ', '')\
                    .replace('пгт. Сарс', 'р.п. Сарс')\
                    .replace('пгт. ', '')\
                    .replace('рп.', '')
                area = val[4].replace('р-н. ', '')
                addr = dictionaries.models.Address.objects.get(area__contains=area, city__contains=city, street=street)
                house, created = dictionaries.models.House.objects.get_or_create(address=addr, number=val[8])
                insp = inspections.models.Inspection.objects.get(gis_gkh_number=val[1])
                insp.houses.add(house)
                insp.save()
            except dictionaries.models.Address.DoesNotExist:
                print("Не найдена запись: " + area + city + street)
            except inspections.models.Inspection.DoesNotExist:
                print("Не найдена проверка: " + val[1])
            except MultipleObjectsReturned:
                print("Несколько адресов " + area + city + street)

        row = row + 1


def import_order_from_gis_gkh(file):
    rb = xlrd.open_workbook(file)
    sheet = rb.sheet_by_index(2)
    row = 2
    while row < sheet.nrows and sheet.row_values(row)[0] != '':
        val = sheet.row_values(row)
        try:
            insp = inspections.models.Inspection.objects.get(gis_gkh_number=val[1])
            order, created = inspections.models.Precept.objects.get_or_create(parent=insp, doc_number=val[2], doc_date=datetime.strptime(val[3], '%d.%m.%Y').date())
            if created:
                order.doc_type = 'предписание'
                order.organization = insp.organization
            if val[6] != '':
                order.order_end_date = datetime.strptime(val[6], '%d.%m.%Y').date()
            order.save()
        except inspections.models.Inspection.DoesNotExist:
            print("Not found inspection: " + val[1])
        except MultipleObjectsReturned:
            pass
        row = row + 1


def export_excel(query_set, user_id, get_http_response=False):
    result = analytic.models.ExportResult()
    result.user = dictionaries.models.User.objects.get(django_user__pk=user_id)
    count = query_set.count()
    wb = openpyxl.Workbook()
    ws = wb.worksheets[0]
    ws.title = "iggndb"
    fields = filter.get_model_columns([], query_set.model)
    # заголовок
    for col, field in enumerate(fields):
        ws.cell(1, col + 1).value = field['verbose_name']
    # данные
    for row, item in enumerate(query_set):
        for col, field in enumerate(fields):
            pass
            if field['field'].__class__ == django.db.models.fields.related.ManyToManyField:
                # для полей типа ManyToMany просто перечисляем через запятую все найденные значения
                # это значит, что во второй модели должна быть прописана функция __str__
                val = ''
                f = item
                for p in str(field['prefix'] + field['name']).split('.'):
                    if f is None:
                        continue
                    f = f.__getattribute__(p)
                if f is None:
                    continue
                for i in f.all():
                    if val == '':
                        val = str(i)
                    else:
                        val = val + ',' + str(i)
                ws.cell(row + 2, col + 1).value = val
            else:
                # с этого момента начинаем брать каскадом значения полей
                # например field['prefix'] может быть равен 'organization.org_type.'
                # а field['name'] равен 'text'
                # в таком случае наша задача получить значение поля item.organization.org_type.text
                ws.cell(row + 2, col + 1).value = filter.get_value(item, field['prefix'] + field['name'])
        result.text = "Сделано %s из %s" % (row, count)
        result.save()
    result.text = 'Выгрузка таблицы "' + query_set.model._meta.verbose_name + '" с фильтрацией'
    result.datetime = timezone.now()
    result.file.save(uuid.uuid1().hex+'.xlsx', ContentFile(save_virtual_workbook(wb)))
    result.save()


def import_houses_from_licensing(file):
    file = 'C:\\1.xlsx'
    rb = xlrd.open_workbook(file)
    sheet = rb.sheet_by_name('Сведения об МКД')
    row = 8
    while row < sheet.nrows and sheet.row_values(row)[0] != '':
        row = row + 1
        val = sheet.row_values(row)
        area = val[1].strip()
        place = val[2].strip()
        city = val[3].strip()
        street = val[5].strip()
        number = val[6] if type(val[6]) is str else int(val[6])
        number = normalize_house_number(number)
        addr, created = dictionaries.models.Address.objects.get_or_create(area=area, place=place, city=city, street=street)
        house, created = dictionaries.models.House.objects.get_or_create(address=addr, number=number)
        try:
            org = dictionaries.models.Organization.objects.get(inn=int(val[16]))
            house.organization = org
        except dictionaries.models.Organization.DoesNotExist:
            pass
        house.building_year = int(val[7]) if val[7] else 0
        house.number_of_apartments = int(val[8]) if val[8] else 0
        house.total_area = val[9] if val[9] else 0
        house.living_area = val[10] if val[10] else 0
        house.non_living_area = val[11] if val[11] else 0
        house.changing_doc_number = val[19] if val[19] else None
        house.changing_doc_date = datetime(*xlrd.xldate_as_tuple(val[21], rb.datemode)) if val[21] else None
        house.changing_doc_header = val[22] if val[22] else None
        house.changing_org_date = datetime(*xlrd.xldate_as_tuple(val[24], rb.datemode)) if val[24] else None
        house.agr_conclusion_date = datetime(*xlrd.xldate_as_tuple(val[25], rb.datemode)) if val[25] else None
        house.management_start_date = datetime(*xlrd.xldate_as_tuple(val[26], rb.datemode)) if val[26] else None
        house.exclusion_date = datetime(*xlrd.xldate_as_tuple(val[28], rb.datemode)) if val[28] else None
        house.exclusion_legal_basis = val[29] if val[29] else None
        house.save()

