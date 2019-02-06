from django.db import models
from dictionaries.models import User
from inspections.models import ViolationType, ControlKind, InspectionResult


class ExportResult(models.Model):
    text = models.TextField(null=True)
    datetime = models.DateTimeField(null=True)
    file = models.FileField(upload_to='exports/', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class GeneralReport(models.Model):
    # ���� ����������� ������ ������������ �������, �� ����������� date_begin � date_end
    date_begin = models.DateField(null=True, blank=True, verbose_name='������ ��������� �������')
    date_end = models.DateField(null=True, blank=True, verbose_name='��������� ��������� �������')
    # ���� ����� ������������ ������������� �� ����������� month � year
    month = models.IntegerField(verbose_name='�����', default=0)
    year = models.IntegerField(verbose_name='���', default=0)
    control_kind = models.ForeignKey(ControlKind, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='��� ��������')
    # ������ 1
    houses_total_area = models.IntegerField(verbose_name='������� ������������� ��� � ����� �����', default=0)
    houses_plan_area = models.IntegerField(
        verbose_name='������� ������������� ��� � ����� ����� � ���������� �������� ��������',
        default=0)
    houses_precept_area = models.IntegerField(
        verbose_name='������� ������������� ��� � ����� ����� � ���������� �������� ���������� �����������',
        default=0)
    houses = models.IntegerField(verbose_name='���������� ������������� ��� � ����� �����', default=0)
    doc = models.IntegerField(verbose_name='���������� ������������� ��������', default=0)
    doc_plan = models.IntegerField(verbose_name='���������� ������������� �������� ��������', default=0)
    doc_appeals = models.IntegerField(verbose_name='���������� ������������� �������� �� ���������� �������', default=0)
    doc_prosecutor = models.IntegerField(verbose_name='���������� ������������� �������� �� ���������� �����������',
                                         default=0)
    doc_oms = models.IntegerField(
        verbose_name='���������� ������������� �������� � ��������� ������� �������� ��������������', default=0)
    doc_precept = models.IntegerField(verbose_name='���������� ������������� �������� ���������� �����������',
                                      default=0)
    out = models.IntegerField(verbose_name='���������� �������� �������', default=0)
    out_plan = models.IntegerField(verbose_name='���������� �������� �������� �������', default=0)
    out_appeals = models.IntegerField(verbose_name='���������� �������� ������� �� ���������� �������', default=0)
    out_prosecutor = models.IntegerField(verbose_name='���������� �������� ������� �� ���������� �����������',
                                         default=0)
    out_oms = models.IntegerField(
        verbose_name='���������� �������� ������� � ��������� ������� �������� ��������������', default=0)
    out_physic = models.IntegerField(verbose_name='���������� �������� ������� � ��������� ����������� ����', default=0)
    out_order = models.IntegerField(verbose_name='���������� �������� ������� ���������� �����������', default=0)
    overdue = models.IntegerField(verbose_name='���������� ��������, ����������� � ���������� �����', default=0)
    overdue_doc = models.IntegerField(verbose_name='���������� ������������� ��������, ����������� � ���������� �����',
                                      default=0)
    overdue_out = models.IntegerField(verbose_name='���������� �������� ��������, ����������� � ���������� �����',
                                      default=0)
    # ������ 2 - ���������
    # ������ 3 - ���������� ������������
    exec_doc = models.IntegerField(verbose_name='���������� ������������ �������������� ����������',
                                   default=0)
    act = models.IntegerField(verbose_name='���������� ������������ �����',
                              default=0)
    precept = models.IntegerField(verbose_name='���������� ������������ �����������',
                                  default=0)


class ViolationInGeneralReport(models.Model):
    violation_type = models.ForeignKey(ViolationType, on_delete=models.SET_NULL, null=True,
                                       verbose_name='��� ���������')
    count = models.IntegerField(default=0, verbose_name='���������� ��������� ��������')
    count_to_remove = models.IntegerField(default=0, verbose_name='���������� ��������� � ����������')
    count_of_removed = models.IntegerField(default=0, verbose_name='���������� ��������� �� ����� ���������')
    report = models.ForeignKey(GeneralReport, on_delete=models.SET_NULL, null=True, verbose_name='�����')


class AbstractItemCountInReport(models.Model):
    model_name = models.TextField(verbose_name='��� ������ �����������')
    object_id = models.IntegerField(verbose_name='id �������� ������������')
    count = models.IntegerField(default=0, verbose_name='����������')
    report = models.ForeignKey(GeneralReport, on_delete=models.SET_NULL, null=True, verbose_name='�����')
