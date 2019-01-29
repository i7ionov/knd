# -*- coding: utf-8 -*-
import xlrd, openpyxl
import inspections.models
import dictionaries.models
from django.core.exceptions import MultipleObjectsReturned
from django.utils import timezone
from django.http import HttpResponse
import django
import uuid
from analytic import models
from dictionaries.models import User, House
from django.core.files.base import ContentFile
from openpyxl.writer.excel import save_virtual_workbook
from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib.auth.models import User as DjangoUser
from inspections.models import ViolationInInspection, Inspection
from django.conf import settings


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
        elif dictionaries.models.Organization.objects.filter(ogrn=val[13]).count() == 1:
            # находим ее по огрн
            org = dictionaries.models.Organization.objects.get(ogrn=val[13])
            org.kpp = val[14]
            if val[11] == 'Организация':
                org.org_type_id = 2
            else:
                org.org_type_id = 1
            org.name = val[12]
            org.save()
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

        if val[25] == "Нарушения выявлены":
            insp.violations_quantity = 1
        else:
            insp.violations_quantity = 0
        if val[28] != '':
            insp.act_date = datetime.strptime(val[17], '%d.%m.%Y').date()
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
                order.root_id = insp.root_id
                order.organization = insp.organization
            if val[6] != '':
                order.order_end_date = datetime.strptime(val[6], '%d.%m.%Y').date()
            order.save()
        except inspections.models.Inspection.DoesNotExist:
            print("Not found inspection: " + val[1])
        except MultipleObjectsReturned:
            pass
        row = row + 1