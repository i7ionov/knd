from django.db import models
from django.contrib.auth.models import User as DjangoUser
from mptt.models import MPTTModel, TreeForeignKey
from simple_history.models import HistoricalRecords
from simple_history import register


# Create your models here.


class User(models.Model):
    django_user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='ФИО')
    name_rp = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    position_rp = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    department_rp = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сотрудник"


class AbstractListItem(models.Model):
    text = models.CharField(max_length=500, default="", null=True)

    def __str__(self):
        return self.text

    class Meta:
        abstract = True


# тип организации
class OrganizationType(AbstractListItem):
    pass


class Address(models.Model):
    area = models.CharField(max_length=100, verbose_name='Район')
    place = models.CharField(max_length=100, verbose_name='Муниципальное образование')
    city = models.CharField(max_length=100, verbose_name='Населенный пункт')
    city_weight = models.IntegerField(default=100)
    street = models.CharField(max_length=100, verbose_name='Улица')

    def __str__(self):
        return self.city + self.street

    class Meta:
        verbose_name = "Адрес"


class File(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Файл"


class Organization(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name='Наименование организации')
    inn = models.CharField(max_length=50, blank=True, null=True, verbose_name='ИНН')
    ogrn = models.CharField(max_length=50, blank=True, null=True, verbose_name='ОГРН')
    is_bankrupt = models.BooleanField(default=False, blank=True, verbose_name='Банкрот')
    kpp = models.CharField(max_length=50, null=True, blank=True, verbose_name='КПП')
    org_type = models.ForeignKey(OrganizationType, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Тип организации')
    location_address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Адрес места нахождения')
    telephone = models.CharField(max_length=50, null=True, blank=True, verbose_name='Телефон')
    email = models.CharField(max_length=50, null=True, blank=True, verbose_name='Эл. почта')
    comment = models.CharField(max_length=1000, blank=True, null=True)
    files = models.ManyToManyField(File, blank=True, verbose_name='файлы')
    history = HistoricalRecords(inherit=True)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        return self.name + ', ИНН:' + self.inn

    class Meta:
        verbose_name = "Организация"


class House(models.Model):
    verbose_name = "Дом"
    number = models.CharField(max_length=100, verbose_name='Номер дома')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, verbose_name='Адрес')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, verbose_name='Организация')
    comment = models.CharField(max_length=1000, null=True)
    guid = models.CharField(max_length=100, null=True)
    files = models.ManyToManyField(File, blank=True, verbose_name='файлы')
    history = HistoricalRecords(inherit=True)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        return f'{self.address.place}, {self.address.city}, {self.address.street}, {self.number}'

    class Meta:
        verbose_name = "Дом"


# статьи
class Article(AbstractListItem):
    article_type = models.CharField(max_length=500, default="", null=True)  # тип статьи

    class Meta:
        verbose_name = "Статья"


# класс документа по проверке
class Document(MPTTModel):
    doc_number = models.CharField(max_length=500, verbose_name='номер документа')
    doc_date = models.DateField(verbose_name='дата документа', blank=True)
    doc_type = models.CharField(max_length=500, default="", null=True, verbose_name='тип документа')
    root_id = models.IntegerField(editable=False, default=0, verbose_name='root_id')
    files = models.ManyToManyField(File, blank=True, verbose_name='файлы')
    houses = models.ManyToManyField(House, blank=True, verbose_name='адреса домов')
    organization = models.ForeignKey(Organization, blank=True, on_delete=models.SET_NULL, null=True,
                                     verbose_name='Организация')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            on_delete=models.SET_NULL)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = "Документ"


register(Document)


class WorkingDays(models.Model):
    day = models.DateField(default="2017-01-01")


class Recipient(models.Model):
    email = models.CharField(max_length=500, verbose_name='емейл')
    group = models.CharField(max_length=500, verbose_name='группа')
