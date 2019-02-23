from django.db import models
from dictionaries.models import User, Department
from inspections.models import ViolationType, ControlKind, InspectionResult


class ExportResult(models.Model):
    text = models.TextField(null=True)
    datetime = models.DateTimeField(null=True)
    file = models.FileField(upload_to='exports/', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class GeneralReport(models.Model):
    report_status = models.TextField(null=True, blank=True, verbose_name='Статус формирования отчета')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Сотрудник, запросивший отчет')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True,
                                   verbose_name='Отдел, по которому составляется отчет')
    date = models.DateField(null=True, blank=True, verbose_name='Дата составления отчета')
    # Если составление отчета инициируется вручную, но заполняются date_begin и date_end
    date_begin = models.DateField(null=True, blank=True, verbose_name='Начало отчетного периода')
    date_end = models.DateField(null=True, blank=True, verbose_name='Окончание отчетного периода')
    # Если отчет составляется автоматически то заполняется month и year
    month = models.IntegerField(verbose_name='Месяц', default=0)
    year = models.IntegerField(verbose_name='Год', default=0)
    control_kind = models.ForeignKey(ControlKind, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='вид контроля')
    total_inspections = models.IntegerField(verbose_name='Всего проверок', default=0)
    # Раздел 1
    houses_total_area = models.IntegerField(verbose_name='Площадь обследованных МКД и жилых домов', default=0)
    houses_plan_area = models.IntegerField(
        verbose_name='Площадь обследованных МКД и жилых домов в результате плановых проверок',
        default=0)
    houses_precept_area = models.IntegerField(
        verbose_name='Площадь обследованных МКД и жилых домов в результате проверки исполнения предписаний',
        default=0)
    houses = models.IntegerField(verbose_name='Количество обследованных МКД и жилых домов', default=0)
    doc = models.IntegerField(verbose_name='Количество документарных проверок', default=0)
    doc_plan = models.IntegerField(verbose_name='Количество документарных плановых проверок', default=0)
    doc_appeals = models.IntegerField(verbose_name='Количество документарных проверок по обращениям граждан', default=0)
    doc_prosecutor = models.IntegerField(verbose_name='Количество документарных проверок по требованию прокуратуры',
                                         default=0)
    doc_oms = models.IntegerField(
        verbose_name='Количество документарных проверок в отношении органов местного самоуправления', default=0)
    doc_precept = models.IntegerField(verbose_name='Количество документарных проверок исполнения предписания',
                                      default=0)
    out = models.IntegerField(verbose_name='Количество выездных поверок', default=0)
    out_plan = models.IntegerField(verbose_name='Количество выездных плановых поверок', default=0)
    out_appeals = models.IntegerField(verbose_name='Количество выездных поверок по обращениям граждан', default=0)
    out_prosecutor = models.IntegerField(verbose_name='Количество выездных поверок по требованию прокуратуры',
                                         default=0)
    out_oms = models.IntegerField(
        verbose_name='Количество выездных поверок в отношении органов местного самоуправления', default=0)
    out_physic = models.IntegerField(verbose_name='Количество выездных поверок в отношении физического лица', default=0)
    out_precept = models.IntegerField(verbose_name='Количество выездных поверок исполнения предписания', default=0)
    doc_and_out = models.IntegerField(verbose_name='Количество документарных и выездных проверок', default=0)
    doc_and_out_plan = models.IntegerField(verbose_name='Количество документарных и выездных плановых проверок', default=0)
    doc_and_out_appeals = models.IntegerField(verbose_name='Количество документарных и выездных проверок по обращениям граждан', default=0)
    doc_and_out_prosecutor = models.IntegerField(verbose_name='Количество документарных и выездных проверок по требованию прокуратуры',
                                         default=0)
    doc_and_out_oms = models.IntegerField(
        verbose_name='Количество документарных и выездных проверок в отношении органов местного самоуправления', default=0)
    doc_and_out_precept = models.IntegerField(verbose_name='Количество документарных и выездных проверок исполнения предписания',
                                      default=0)
    overdue = models.IntegerField(verbose_name='Количество проверок, проведенных с нарушением срока', default=0)
    overdue_doc = models.IntegerField(verbose_name='Количество документарных проверок, проведенных с нарушением срока',
                                      default=0)
    overdue_out = models.IntegerField(verbose_name='Количество выездных проверок, проведенных с нарушением срока',
                                      default=0)
    # Раздел 2 - нарушения
    violation_count = models.IntegerField(verbose_name='Количество выявленных нарушений', default=0)
    violation_count_to_remove = models.IntegerField(verbose_name='Количество нарушений к устранению', default=0)
    violation_count_of_removed = models.IntegerField(verbose_name='Количество устраненных нарушений', default=0)
    # Раздел 3 - результаты деятельности
    exec_doc = models.IntegerField(verbose_name='Количество составленных исполнительных документов',
                                   default=0)
    act = models.IntegerField(verbose_name='Количество составленных актов',
                              default=0)
    precept = models.IntegerField(verbose_name='Количество составленных предписаний',
                                  default=0)


class ViolationInGeneralReport(models.Model):
    violation_type = models.ForeignKey(ViolationType, on_delete=models.SET_NULL, null=True,
                                       verbose_name='тип нарушения')
    count = models.IntegerField(default=0, verbose_name='количество нарушений выявлено')
    count_to_remove = models.IntegerField(default=0, verbose_name='количество нарушений к устранению')
    count_of_removed = models.IntegerField(default=0, verbose_name='количество нарушений по факту устранено')
    report = models.ForeignKey(GeneralReport, on_delete=models.SET_NULL, null=True, verbose_name='Отчет')


class AbstractItemCountInReport(models.Model):
    model_name = models.TextField(verbose_name='имя модели справочника')
    object_id = models.IntegerField(verbose_name='id элемента справочкинка')
    text = models.TextField(verbose_name='наименование элемента справочника')
    count = models.IntegerField(default=0, verbose_name='количество')
    report = models.ForeignKey(GeneralReport, on_delete=models.SET_NULL, null=True, verbose_name='Отчет')
