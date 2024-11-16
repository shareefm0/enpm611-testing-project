import unittest
from unittest.mock import patch
from feature_4 import EventAnalysis
from model import Issue, Event


class TestEventAnalysis(unittest.TestCase):

    @patch('feature_4.DataLoader')
    def test_run(self, mock_data_loader):
        issues = [
            Issue({'state': 'open',
                   'events': [{'event_date': '2021-01-01T12:00:00Z'}, {'event_date': '2021-01-02T12:00:00Z'}]}),
            Issue({'state': 'closed', 'events': [{'event_date': '2021-01-01T13:00:00Z'}]}),
            Issue({'state': 'open', 'events': [{'event_date': None}]})
        ]
        mock_data_loader.return_value.get_issues.return_value = issues

        analysis = EventAnalysis()
        with patch('matplotlib.pyplot.show'):
            analysis.run()
        # Since plotting does not return values, this test ensures no exceptions are raised.

    def test_event_analysis_with_none_event_date(self):
        print("ERROR_NOTE: EventAnalysis fails with a TypeError when event.event_date is None.")
        issues = [Issue({'state': 'open', 'events': [{'event_date': None}]})]
        with patch('data_loader.DataLoader.get_issues', return_value=issues):
            analysis = EventAnalysis()
            # This will raise an error when attempting to create a DataFrame with None dates
            analysis.run()


if __name__ == '__main__':
    unittest.main()
