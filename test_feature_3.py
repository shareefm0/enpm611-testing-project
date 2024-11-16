import unittest
from unittest.mock import patch
from feature_3 import UserAnalyzer
from model import Issue
from datetime import datetime


class TestUserAnalyzer(unittest.TestCase):

    @patch('feature_3.DataLoader')
    def test_user_issue_count(self, mock_data_loader):
        issues = [
            Issue({'state': 'open', 'creator': 'user1', 'labels': ['bug'], 'created_date': '2021-01-01T12:00:00Z'}),
            Issue({'state': 'closed', 'creator': 'user2', 'labels': ['enhancement'],
                   'created_date': '2021-01-02T12:00:00Z'}),
            Issue({'state': 'open', 'creator': 'user1', 'labels': [], 'created_date': '2021-01-03T12:00:00Z'}),
        ]
        mock_data_loader.return_value.get_issues.return_value = issues

        analyzer = UserAnalyzer()
        with patch('builtins.print') as mock_print:
            analyzer.user_issue_count('user1')
            mock_print.assert_any_call('user1 has created 2 issue(s):')
            self.assertEqual(mock_print.call_count, 3)  # One for the summary, two for the issues (filtered by user1)

    def test_user_analyzer_missing_run_method(self):
        print("ERROR_NOTE: UserAnalyzer does not have a run() method, but it's called in __main__.")
        analyzer = UserAnalyzer()
        # This will raise an AttributeError because 'run' method is not defined in UserAnalyzer
        analyzer.run()


if __name__ == '__main__':
    unittest.main()
