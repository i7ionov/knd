# Create your tasks here
from __future__ import absolute_import, unicode_literals

from analytic.general_report import iterate_inspections
from analytic.models import GeneralReport
from iggndb.celery import app
from datetime import datetime
from inspections.models import Inspection


@app.task
def generate_general_report_period(user_id, date_begin, date_end, control_kind_id=None, department_id=None):
    report = GeneralReport(report_status='Формируется...', user_id=user_id, date=datetime.now(), date_begin=date_begin,
                           date_end=date_end)
    inspections = Inspection.objects.filter(act_date__range=(date_begin, date_end))
    # исключаем тестовые проверки
    inspections = inspections.exclude(inspection_result_id=12).exclude(control_form__id=4).exclude(
        control_form__id=5)
    if control_kind_id:
        inspections = inspections.filter(control_kind_id=control_kind_id)
        report.control_kind_id = control_kind_id
    if department_id:
        inspections = inspections.filter(inspector__department_id=department_id)
        report.department_id = department_id
    iterate_inspections(inspections, report)
    return report


@app.task
def generate_general_report_month(month, year):
    pass


