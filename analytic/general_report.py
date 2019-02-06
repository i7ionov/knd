from .models import GeneralReport, ViolationInGeneralReport, AbstractItemCountInReport
from inspections.models import Inspection


def generate_general_report_period(date_begin, date_end, control_kind_id):
    report = GeneralReport()
    inspections = Inspection.objects.filter(doc_date__range=(date_begin, date_end)).filter(control_kind_id=control_kind_id)
    iterate_inspections(inspections, report)
    return report


def generate_general_report_month(month, year):
    pass


def iterate_inspections(inspections, report):
    houses_list = []
    for insp in inspections:
        # пополним id домов в списке домов
        for house in insp.houses.all():
            if house.id not in houses_list:
                houses_list.append(house.id)
            # если проверка документарная
            if 'документарная' in insp.control_form.text.lower():
                report.doc += 1
                # если проверка плановая
                if insp.control_plan.id == 2:
                    report.doc_plan += 1
                if insp.legal_basis:
                    if 'обращ' in insp.legal_basis.text.lower():
                        report.doc_appeals += 1
                    elif 'прокур' in insp.legal_basis.text.lower():
                        report.doc_prosecutor += 1
                    elif 'предпис' in insp.legal_basis.text.lower():
                        report.doc_order += 1
                if insp.organization and 'Орган местного самоуправления' in insp.organization.org_type.text:
                    report.doc_oms += 1
            # если проверка выездная
            if 'выездная' in insp.control_form.text.lower():
                report.out += 1
                # если проверка плановая
                if insp.control_plan.id == 2:
                    report.out_plan += 1
                if insp.legal_basis:
                    if 'обращ' in insp.legal_basis.text.lower():
                        report.out_appeals += 1
                    elif 'прокур' in insp.legal_basis.text.lower():
                        report.out_prosecutor += 1
                    elif 'предпис' in insp.legal_basis.text.lower():
                        report.out_order += 1
                if insp.organization and 'Орган местного самоуправления' in insp.organization.org_type.text:
                    report.out_oms += 1
            # если дата акта больше дата окончания проверки
            if insp.date_end and insp.act_date and insp.date_end < insp.act_date:
                report.overdue += 1
                if 'выездная' in insp.control_form.text.lower():
                    report.overdue_out += 1
                if 'документарная' in insp.control_form.text.lower():
                    report.overdue_doc += 1
            if insp.inspection_result:
                insp_rexult, created = AbstractItemCountInReport.objects.get_or_create(model_name='inspection_result', object_id=insp.inspection_result.id)

            report.save()
            # статистика по выявленным нарушениям
            for v in insp.violationininspection_set.all():
                violation, created = ViolationInGeneralReport.objects.get_or_create(violation_type_id=v.id,
                                                                                        report=report)
                violation.count += v.count
                violation.save()
            # статистика по исправленным нарушениям
            for o in insp.children.all():
                if o.order:
                    for v in o.order.violationinorder_set.all():
                        violation, created = ViolationInGeneralReport.objects.get_or_create(violation_type_id=v.id,
                                                                                            report=report)
                        violation.count_to_remove += v.count_to_remove
                        violation.count_of_removed += v.count_of_removed
                        violation.save()
    return report
