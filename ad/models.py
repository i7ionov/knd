from django.db import models
from dictionaries.models import Organization, Article, Document, House, User, Officer
from inspections.models import Inspection, Precept
from simple_history.models import HistoricalRecords


class AbstractListItem(models.Model):
    text = models.CharField(max_length=500, default="", null=True)

    def __str__(self):
        return self.text

    class Meta:
        abstract = True


# суд
class Court(models.Model):
    name = models.CharField(max_length=500, default="", null=True, verbose_name='Наименование суда')
    address = models.CharField(max_length=500, default="", null=True, verbose_name='Адрес')
    oktmo = models.CharField(max_length=20, default="", null=True, verbose_name='ОКТМО')
    email = models.CharField(max_length=50, default="", null=True, verbose_name='Почта')
    telephone = models.CharField(max_length=50, default="", null=True, verbose_name='Телефон')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Суд"


# ФССП
class FSSP(models.Model):
    name = models.CharField(max_length=500, default="", null=True, verbose_name='Наименование суда')
    address = models.CharField(max_length=500, default="", null=True, verbose_name='Адрес')
    oktmo = models.CharField(max_length=20, default="", null=True, verbose_name='ОКТМО')
    email = models.CharField(max_length=50, default="", null=True, verbose_name='Почта')
    telephone = models.CharField(max_length=50, default="", null=True, verbose_name='Телефон')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Суд"


# решение
class Adjudication(AbstractListItem):
    pass

    class Meta:
        verbose_name = "Решение"


# результат исполнительного производства
class ExecutionResult(AbstractListItem):
    pass

    class Meta:
        verbose_name = "Результат исп производства"


# запись о исполнительном производстве
class Execution(Document):
    is_forced = models.BooleanField(default=False, verbose_name='Принудительная оплата')
    payment_date = models.DateField(null=True, verbose_name='Дата оплаты')
    payment_amount = models.IntegerField(default=0, verbose_name='Сумма оплаты')
    referring_to_instance_date = models.DateField(null=True, verbose_name='Дата направления в инстанцию')
    fssp = models.ForeignKey(FSSP, on_delete=models.SET_NULL, null=True, verbose_name='ФССП')
    execution_number = models.CharField(max_length=500, default="", null=True, verbose_name='Номер исполнительного производства')
    execution_date = models.DateField(null=True, verbose_name='Дата исполнительного производства')
    execution_stop_date = models.DateField(null=True, verbose_name='Дата окончания исполнительного производства')
    execution_result = models.ForeignKey(ExecutionResult, on_delete=models.SET_NULL, null=True, verbose_name='Результат')
    comment = models.TextField(default='', verbose_name='Комментарий')
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = "Запись исполнительного производства"


# стадия исполнительного производства
class ADStage(AbstractListItem):
    short_text = models.CharField(max_length=500, default="", null=True)

    class Meta:
        verbose_name = "Стадия исп. произв."


# запись об административном делопроизводстве
class ADRecord(Document):
    ad_type = models.IntegerField(default=0)  # информация, где проходит расмотрение (0-м/c, 1-инспекция, 2-обжалование)
    ad_stage = models.ForeignKey(ADStage, on_delete=models.SET_NULL, null=True,  blank=True, verbose_name='Стадия рассмотрения административного дела')
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Статья')
    protocol_date = models.DateField(null=True, blank=True, verbose_name='Дата протокола')
    referring_to_instance_date = models.DateField(null=True, blank=True, verbose_name='Дата направления в инстанцию')
    court = models.ForeignKey(Court, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Инстанция')
    adjudication = models.ForeignKey(Adjudication, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Решение')
    adjudication_amount_of_fine = models.IntegerField(default=0, blank=True, verbose_name='Размер штрафа')
    adjudication_date = models.DateField(null=True, blank=True, verbose_name='Дата вынесения решения')
    adjudication_start_date = models.DateField(null=True, blank=True, verbose_name='Дата вступления в силу')
    date_of_receipt_unlegal = models.DateField(null=True, blank=True, verbose_name='Дата поступления постан не вступившего в законную силу')
    date_of_receipt_legal = models.DateField(null=True, blank=True, verbose_name='Дата поступления постан вступившего в законную силу')
    publish_gisgkh_date = models.DateField(null=True, blank=True, verbose_name='Дата публикации в ГИС ЖКХ')
    publish_erp_date = models.DateField(null=True, blank=True, verbose_name='Дата публикации в ЕРП')
    box_number = models.CharField(max_length=500, blank=True, default="", null=True, verbose_name='Номер коробки в архиве')
    uin = models.CharField(max_length=50, blank=True, default="", null=True,
                             verbose_name='ОКТМО')
    inspector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='инспектор')
    officer = models.ForeignKey(Officer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='должностное лицо')
    comment = models.TextField(default='', blank=True, verbose_name='Комментарий')
    has_appeal = models.BooleanField(default=False, blank=True, verbose_name='Имеет обжалование')
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = "Запись АД"
