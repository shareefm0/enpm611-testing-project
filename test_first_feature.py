import unittest
from unittest.mock import patch
from first_feature import MonthlyIssueAnalyser
from model import Issue
from datetime import datetime


class TestMonthlyIssueAnalyser(unittest.TestCase):

    @patch('first_feature.DataLoader')
    def test_analyse_all_years(self, mock_data_loader):
        # Mock issues with different dates
        issues = [
            Issue({'state': 'open', 'created_date': '2021-01-15T12:00:00Z'}),
            Issue({'state': 'open', 'created_date': '2021-02-20T12:00:00Z'}),
            Issue({'state': 'open', 'created_date': '2022-01-10T12:00:00Z'}),
            Issue({'state': 'closed', 'created_date': None})  # Issue with no created_date
        ]
        mock_data_loader.return_value.get_issues.return_value = issues

        analyser = MonthlyIssueAnalyser()
        with patch('builtins.print') as mock_print:
            with patch('matplotlib.pyplot.show'):
                analyser.analyse()
            mock_print.assert_any_call('Skipping issue with no created_date')
            mock_print.assert_any_call(
                'Month-Wise breakdown of the total number of issues reported across all years is 3.')

    @patch('first_feature.DataLoader')
    def test_analyse_specific_year(self, mock_data_loader):
        # Mock issues with different dates
        issues = [
            Issue({'state': 'open', 'created_date': '2021-01-15T12:00:00Z'}),
            Issue({'state': 'closed', 'created_date': '2021-02-20T12:00:00Z'}),
            Issue({'state': 'open', 'created_date': '2022-01-10T12:00:00Z'}),
        ]
        mock_data_loader.return_value.get_issues.return_value = issues

        analyser = MonthlyIssueAnalyser(year=2021)
        with patch('builtins.print') as mock_print:
            with patch('matplotlib.pyplot.show'):
                analyser.analyse()
            mock_print.assert_any_call('The total number of issues reported in year 2021 is 2.')

    def test_monthly_issue_analyser_missing_created_date(self):
        print("ERROR_NOTE: MonthlyIssueAnalyser fails with ValueError when issue.created_date is invalid.")
        issue = Issue({'state': 'open'})
        issue.created_date = 'invalid'
        with patch('data_loader.DataLoader.get_issues', return_value=[issue]):
            analyser = MonthlyIssueAnalyser()
            analyser.analyse()


if __name__ == '__main__':
    unittest.main()
