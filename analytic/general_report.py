from datetime import datetime
from .models import GeneralReport, ViolationInGeneralReport, AbstractItemCountInReport
from inspections.models import Inspection


def iterate_inspections(inspections, report):
    houses_list = []
    for insp in inspections:
        report.total_inspections += 1
        # пополним id домов в списке домов
        for house in insp.houses.all():
            if house.id not in houses_list:
                houses_list.append(house.id)
                report.houses += 1
                report.houses_total_area += house.total_area
                # если проверка плановая
                if insp.control_plan and insp.control_plan.id == 2:
                    report.houses_plan_area += house.total_area
                if insp.legal_basis and 'предпис' in insp.legal_basis.text.lower():
                    report.houses_precept_area += house.total_area
        # если проверка документарная
        if insp.control_form_id == 2:
            report.doc += 1
            # если проверка плановая
            if insp.control_plan and insp.control_plan.id == 2:
                report.doc_plan += 1
            if insp.legal_basis:
                if 'обращ' in insp.legal_basis.text.lower():
                    report.doc_appeals += 1
                elif 'прокур' in insp.legal_basis.text.lower():
                    report.doc_prosecutor += 1
                elif 'предпис' in insp.legal_basis.text.lower():
                    report.doc_precept += 1
            if insp.organization and 'Орган местного самоуправления' in insp.organization.org_type.text:
                report.doc_oms += 1
        # если проверка выездная
        if insp.control_form_id == 1:
            report.out += 1
            # если проверка плановая
            if insp.control_plan and insp.control_plan.id == 2:
                report.out_plan += 1
            if insp.legal_basis:
                if 'обращ' in insp.legal_basis.text.lower():
                    report.out_appeals += 1
                elif 'прокур' in insp.legal_basis.text.lower():
                    report.out_prosecutor += 1
                elif 'предпис' in insp.legal_basis.text.lower():
                    report.out_precept += 1
            if insp.organization and 'Орган местного самоуправления' in insp.organization.org_type.text:
                report.out_oms += 1
        # если проверка документарная и выездная
        if insp.control_form_id == 3:
            report.doc_and_out += 1
            # если проверка плановая
            if insp.control_plan and insp.control_plan.id == 2:
                report.doc_and_out_plan += 1
            if insp.legal_basis:
                if 'обращ' in insp.legal_basis.text.lower():
                    report.doc_and_out_appeals += 1
                elif 'прокур' in insp.legal_basis.text.lower():
                    report.doc_and_out_prosecutor += 1
                elif 'предпис' in insp.legal_basis.text.lower():
                    report.doc_and_out_precept += 1
            if insp.organization and 'Орган местного самоуправления' in insp.organization.org_type.text:
                report.doc_and_out_oms += 1
        # если дата акта больше дата окончания проверки
        if insp.date_end and insp.act_date and insp.date_end < insp.act_date:
            report.overdue += 1
            if 'выездная' in insp.control_form.text.lower():
                report.overdue_out += 1
            if 'документарная' in insp.control_form.text.lower():
                report.overdue_doc += 1
        if insp.act_date:
            report.act += 1
            report.exec_doc += 1
        for c in insp.children.all():
            if c.doc_type == 'предписание':
                report.precept += 1
                report.exec_doc += 1
        report.save()
        if insp.inspection_result:
            insp_result, created = AbstractItemCountInReport.objects.get_or_create(model_name='inspection_result',
                                                                                   object_id=insp.inspection_result.id,
                                                                                   report=report,
                                                                                   text=insp.inspection_result.text)
            insp_result.count += 1
            insp_result.save()
        # статистика по выявленным нарушениям
        for v in insp.violationininspection_set.all():
            if v.violation_type.children.count() == 0:
                violation, created = ViolationInGeneralReport.objects.get_or_create(violation_type_id=v.violation_type.id,
                                                                                report=report)
                violation.count += v.count
                report.violation_count += v.count
                violation.save()
        # статистика по исправленным нарушениям
        for p in insp.children.all():
            if p.doc_type == 'предписание':
                for v in p.precept.violationinprecept_set.all():
                    if v.violation_type.children.count == 0:
                        violation, created = ViolationInGeneralReport.objects.get_or_create(violation_type_id=v.violation_type.id,
                                                                                        report=report)
                        violation.count_to_remove += v.count_to_remove
                        violation.count_of_removed += v.count_of_removed
                        report.violation_count_to_remove += v.count_to_remove
                        report.violation_count_of_removed += v.count_of_removed
                        violation.save()

    report.report_status = 'Завершен'
    report.save()
    return report
