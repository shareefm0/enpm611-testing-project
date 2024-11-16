import unittest
from unittest.mock import patch
from example_analysis import ExampleAnalysis
from model import Issue, Event


class TestExampleAnalysis(unittest.TestCase):

    @patch('example_analysis.DataLoader')
    def test_run_no_user(self, mock_data_loader):
        # Mock issues with 'creator' and 'state'
        issues = [
            Issue({'creator': 'user1', 'state': 'open', 'events': [{'author': 'user1'}, {'author': 'user2'}]}),
            Issue({'creator': 'user2', 'state': 'closed', 'events': [{'author': 'user1'}]})
        ]
        mock_data_loader.return_value.get_issues.return_value = issues

        analysis = ExampleAnalysis()
        with patch('builtins.print') as mock_print:
            with patch('matplotlib.pyplot.show'):
                analysis.run()
            mock_print.assert_any_call('\n\nFound 3 events across 2 issues.\n\n')

    @patch('example_analysis.DataLoader')
    @patch('example_analysis.config.get_parameter', return_value='user1')
    def test_run_with_user(self, mock_get_parameter, mock_data_loader):
        # Mock issues with 'creator' and 'state'
        issues = [
            Issue({'creator': 'user1', 'state': 'open', 'events': [{'author': 'user1'}, {'author': 'user2'}]}),
            Issue({'creator': 'user2', 'state': 'closed', 'events': [{'author': 'user1'}]})
        ]
        mock_data_loader.return_value.get_issues.return_value = issues

        analysis = ExampleAnalysis()
        with patch('builtins.print') as mock_print:
            with patch('matplotlib.pyplot.show'):
                analysis.run()
            mock_print.assert_any_call('\n\nFound 2 events across 2 issues for user1.\n\n')

    def test_example_analysis_with_none_creator(self):
        print("ERROR_NOTE: ExampleAnalysis fails with an IndexError when issue.creator is None.")
        issues = [
            Issue({'state': 'open', 'creator': None, 'events': [{'author': 'user1'}]}),
        ]
        with patch('data_loader.DataLoader.get_issues', return_value=issues):
            analysis = ExampleAnalysis()
            # This will raise an IndexError when building the DataFrame with a None 'creator'
            analysis.run()


if __name__ == '__main__':
    unittest.main()
