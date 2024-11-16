import unittest
from unittest.mock import patch, mock_open

import data_loader
from model import Issue


class TestDataLoader(unittest.TestCase):

    def setUp(self):
        # Reset the singleton issues list
        data_loader._ISSUES = None

    @patch('config.get_parameter')
    @patch('builtins.open', new_callable=mock_open, read_data='[{"number": 1, "state": "open"}]')
    def test_get_issues(self, mock_file, mock_get_parameter):
        mock_get_parameter.return_value = '/home/user/project/data.json'

        loader = data_loader.DataLoader()
        issues = loader.get_issues()

        self.assertEqual(len(issues), 1)
        self.assertIsInstance(issues[0], Issue)
        self.assertEqual(issues[0].number, 1)
        self.assertEqual(issues[0].state, 'open')

    @patch('config.get_parameter', return_value=None)
    def test_init_no_data_path(self, mock_get_parameter):
        with self.assertRaises(TypeError):
            loader = data_loader.DataLoader()
            loader.get_issues()

    @patch('config.get_parameter', return_value='/invalid/path.json')
    def test_load_file_not_found(self, mock_get_parameter):
        loader = data_loader.DataLoader()
        with self.assertRaises(FileNotFoundError):
            loader.get_issues()

    @patch('config.get_parameter', return_value='/path/to/data.json')
    @patch('builtins.open', side_effect=Exception('Unexpected Error'))
    def test_load_exception(self, mock_open, mock_get_parameter):
        loader = data_loader.DataLoader()
        with self.assertRaises(Exception):
            loader.get_issues()

    def test_data_loader_no_data_path_raises_typeerror(self):
        print("ERROR_NOTE: data_loader fails ungracefully when ENPM611_PROJECT_DATA_PATH is not set, "
              "leading to a TypeError when open() is called.")
        with patch('config.get_parameter', return_value=None):
            loader = data_loader.DataLoader()
            loader.get_issues()


if __name__ == '__main__':
    unittest.main()
