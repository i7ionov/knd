from analytic.general_report import generate_general_report_period
from iggndb.tests.base import BaseTest


class GeneralReportTest(BaseTest):
    def test_general_report_returns_valid_values(self):
        report = generate_general_report_period(self.month_ago, self.month_later, self.control_kind_gn, self.dep1)
        self.fail(report.houses)
