import unittest
from unittest.mock import patch
from feature_2 import TopLabelsAnalyzer
from model import Issue


class TestTopLabelsAnalyzer(unittest.TestCase):

    @patch('feature_2.DataLoader')
    def test_analyse_with_label(self, mock_data_loader):
        issues = [
            Issue({'state': 'open', 'labels': ['bug', 'enhancement']}),
            Issue({'state': 'closed', 'labels': ['bug']}),
            Issue({'state': 'open', 'labels': ['question']}),
        ]
        mock_data_loader.return_value.get_issues.return_value = issues

        analyzer = TopLabelsAnalyzer(label='bug')
        with patch('builtins.print') as mock_print:
            with patch('matplotlib.pyplot.show'):
                analyzer.analyse()
            mock_print.assert_any_call("Count for label 'bug': 2")

    @patch('feature_2.DataLoader')
    def test_analyse_label_not_present(self, mock_data_loader):
        issues = [
            Issue({'state': 'open', 'labels': ['enhancement']}),
            Issue({'state': 'closed', 'labels': ['question']}),
        ]
        mock_data_loader.return_value.get_issues.return_value = issues

        analyzer = TopLabelsAnalyzer(label='bug')
        with patch('builtins.print') as mock_print:
            analyzer.analyse()
            mock_print.assert_any_call("Label 'bug' not present in the data.")

    @patch('feature_2.DataLoader')
    def test_analyse_top_labels(self, mock_data_loader):
        issues = [
            Issue({'state': 'open', 'labels': ['bug']}),
            Issue({'state': 'closed', 'labels': ['bug']}),
            Issue({'state': 'open', 'labels': ['enhancement']}),
        ]
        mock_data_loader.return_value.get_issues.return_value = issues

        analyzer = TopLabelsAnalyzer()
        with patch('builtins.print') as mock_print:
            with patch('matplotlib.pyplot.show'):
                analyzer.analyse()
            mock_print.assert_any_call("Displaying top 50 labels.")

    def test_top_labels_analyzer_issue_with_none_labels(self):
        print("ERROR_NOTE: TopLabelsAnalyzer fails with TypeError when issue.labels is None.")
        issues = [Issue({'state': 'open', 'labels': None})]
        with patch('data_loader.DataLoader.get_issues', return_value=issues):
            analyzer = TopLabelsAnalyzer()
            analyzer.analyse()


if __name__ == '__main__':
    unittest.main()
