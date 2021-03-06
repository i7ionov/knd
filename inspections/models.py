from datetime import datetime

from dictionaries.models import Organization, House, User, Article, File, Document, Department
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from simple_history.models import HistoricalRecords
from django.dispatch import receiver
from simple_history.signals import (
    pre_create_historical_record,
    post_create_historical_record
)


class SerialField(object):
    def db_type(self, connection):
        return 'serial'


class AbstractListItem(models.Model):
    text = models.TextField(default="", null=True)

    def __str__(self):
        return self.text

    class Meta:
        abstract = True


# предмет проверки
class InspectionSubject(AbstractListItem):
    pass


# предмет проверки
class InspectionTask(AbstractListItem):
    pass


# предмет проверки
class LegalBasis(AbstractListItem):
    pass


# вид контроля
class ControlKind(AbstractListItem):
    pass


# форма контроля
class ControlForm(AbstractListItem):
    pass


# вид проверки
class ControlPlan(AbstractListItem):
    pass


# причина непроведения проверки
class InspectionResult(AbstractListItem):
    pass


# статус предписания
class PreceptStatus(AbstractListItem):
    pass


# информация об отмене результатов проверки
class Cancellation(AbstractListItem):
    pass


# результат исполнения предписания
class PreceptResult(AbstractListItem):
    pass


# результат исполнения предписания
class InspectionType(AbstractListItem):
    pass


# нарушения
class ViolationType(MPTTModel):
    text = models.CharField(max_length=200, verbose_name='Текст нарушения')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            on_delete=models.SET_NULL)
    is_vagrant = models.BooleanField(default=False, verbose_name='Грубое нарушение')

    class MPTTMeta:
        order_insertion_by = ['text']

    def __str__(self):
        if self.parent:
            return self.parent.text + self.text
        else:
            return self.text

    class Meta:
        verbose_name = "Нарушение"


# 
class Inspection(Document):
    inspection_type = models.ForeignKey(InspectionType, on_delete=models.SET_NULL, null=True, blank=True,
                                        verbose_name='тип проверки')  # первичная, проверка исполнения предписания
    legal_basis = models.ForeignKey(LegalBasis, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='основание для проверки')
    control_kind = models.ForeignKey(ControlKind, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='вид контроля')
    control_form = models.ForeignKey(ControlForm, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='форма проверки')  # выездная, документарная
    control_plan = models.ForeignKey(ControlPlan, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='вид проверки')  # плановая, внеплановая
    inspection_subjects = models.ManyToManyField(InspectionSubject, verbose_name='предмет проверки', blank=True)
    inspection_tasks = models.ManyToManyField(InspectionTask, verbose_name='задачи проверки', blank=True)
    inspector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='инспектор')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='отдел')
    date_begin = models.DateField(null=True, blank=True, verbose_name='начало проведения проверки')
    date_end = models.DateField(null=True, blank=True, verbose_name='окончание проведения проверки')
    comment = models.TextField(default="", blank=True, verbose_name='комментарий')
    gis_gkh_number = models.TextField(default="", blank=True, verbose_name='номер в ГИС ЖКХ')
    erp_number = models.TextField(default="", blank=True, verbose_name='номер в EРП')
    act_date = models.DateField(null=True, blank=True, verbose_name='дата акта')
    inspection_result = models.ForeignKey(InspectionResult, on_delete=models.SET_NULL, null=True, blank=True,
                                          verbose_name='Результат проверки')
    cancellation = models.ForeignKey(Cancellation, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='Информация об отмене результатов проверки')
    violations_quantity = models.IntegerField(default=0, blank=True, verbose_name='количество нарушений')
    no_preception_needed = models.BooleanField(default=False, verbose_name='Предписание не требуется')
    RPN_notification = models.CharField(max_length=100, null=True, blank=True,
                                        verbose_name='информация о направлении в Роспотребнадзор')
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def update_inspection_type(self):
        type = 'Проверка исполнения предписания' if self.parent else 'Первичная'
        self.inspection_type = InspectionType.objects.get(text=type)
        self.save()

    class Meta:
        permissions = (("can_change_others_inspections", "Сan change others inspections"),)
        verbose_name = "Проверка"


class Precept(Document):
    precept_begin_date = models.DateField(null=True, blank=True, verbose_name='дата начала исполнения предписания')
    precept_end_date = models.DateField(null=True, blank=True, verbose_name='дата окончания исполнения предписания')
    precept_result = models.ForeignKey(PreceptResult, on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name='результат предписания')
    recalculation = models.IntegerField(null=True, blank=True,
                                        verbose_name='сумма перерасчета')
    prolongation_date = models.DateField(null=True, blank=True,
                                         verbose_name='дата окончания исполнения предписания с продлением')
    days_to_start_new_inspection = models.IntegerField(null=True, blank=True,
                                                       verbose_name='Дней до запуска проверки')
    comment = models.TextField(default="", blank=True)  # комментарий
    history = HistoricalRecords()

    def update_days_to_start_new_inspection(self):
        if self.children.filter(
                doc_type='проверка').count() > 0 or self.precept_result and self.precept_result.text != 'Продлено':
            self.days_to_start_new_inspection = None
        else:
            if self.prolongation_date:
                days = self.prolongation_date - datetime.now().date()
            elif self.precept_end_date:
                days = self.precept_end_date - datetime.now().date()
            else:
                return
            self.days_to_start_new_inspection = int(days.days)
        self.save()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = "Предписание"


class ViolationInInspection(models.Model):
    violation_type = models.ForeignKey(ViolationType, on_delete=models.SET_NULL, null=True,
                                       verbose_name='тип нарушения')
    count = models.IntegerField(default=0, verbose_name='количество нарушений')
    inspection = models.ForeignKey(Inspection, on_delete=models.SET_NULL, null=True, verbose_name='проверка')

    def _get_count_has_precept(self):
        result = 0
        for v in ViolationInPrecept.objects.filter(precept__parent_id=self.inspection.id) \
                .filter(violation_type=self.violation_type):
            result = result + v.count_to_remove
        return result

    count_has_precept = property(_get_count_has_precept)

    class Meta:
        verbose_name = "Выявленные нарушения"

    def __str__(self):
        return self.violation_type.text


class ViolationInPrecept(models.Model):
    violation_type = models.ForeignKey(ViolationType, on_delete=models.SET_NULL, null=True,
                                       verbose_name='тип нарушения')
    count_to_remove = models.IntegerField(default=0, verbose_name='количество нарушений к устранению')
    count_of_removed = models.IntegerField(default=0, verbose_name='количество нарушений по факту устранено')
    precept = models.ForeignKey(Precept, on_delete=models.SET_NULL, null=True, verbose_name='предписание')

    def _get_count_in_inspection(self):
        inspection = Inspection.objects.get(id=self.precept.parent.id)
        result = inspection.violationininspection_set.get(violation_type_id=self.violation_type_id).count
        return result

    count_in_inspection = property(_get_count_in_inspection)

    class Meta:
        verbose_name = "Нарушения в предписании"
