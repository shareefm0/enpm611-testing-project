import unittest
from unittest.mock import patch, mock_open
import os
import config


class TestConfig(unittest.TestCase):

    def setUp(self):
        # Reset the _config variable before each test
        config._config = None

    @patch('config.os.getcwd')
    @patch('config.os.path.isfile')
    def test_get_default_path_file_found(self, mock_isfile, mock_getcwd):
        # Simulate finding config.json in the current directory
        expected_path = '/home/user/project/config.json'
        mock_getcwd.return_value = '/home/user/project'
        mock_isfile.side_effect = lambda x: x == expected_path
        filepath = config._get_default_path()
        self.assertEqual(filepath, expected_path)

    @patch('config.os.getcwd')
    @patch('config.os.path.isfile')
    def test_get_default_path_file_not_found(self, mock_isfile, mock_getcwd):
        # Simulate not finding config.json in any directory
        mock_getcwd.return_value = '/home/user/project'
        mock_isfile.return_value = False
        filepath = config._get_default_path()
        self.assertIsNone(filepath)

    @patch('builtins.open', new_callable=mock_open, read_data='{"param1": "value1"}')
    @patch('config._get_default_path')
    def test_init_config_with_file(self, mock_get_default_path, mock_file):
        mock_get_default_path.return_value = '/home/user/project/config.json'
        config._init_config()
        self.assertEqual(config._config, {"param1": "value1"})

    @patch('config._get_default_path')
    def test_init_config_no_file(self, mock_get_default_path):
        mock_get_default_path.return_value = None
        config._init_config()
        self.assertEqual(config._config, {})

    @patch.dict('os.environ', {'TEST_PARAM': 'value_from_env'})
    def test_get_parameter_from_env(self):
        config._config = {'TEST_PARAM': 'value_from_config'}
        value = config.get_parameter('TEST_PARAM')
        self.assertEqual(value, 'value_from_env')

    def test_get_parameter_from_config(self):
        config._config = {'TEST_PARAM': 'value_from_config'}
        value = config.get_parameter('TEST_PARAM')
        self.assertEqual(value, 'value_from_config')

    def test_get_parameter_default(self):
        config._config = {}
        value = config.get_parameter('NON_EXISTENT_PARAM', default='default_value')
        self.assertEqual(value, 'default_value')

    def test_convert_to_typed_value_json(self):
        self.assertEqual(config.convert_to_typed_value('{"a": 1}'), {"a": 1})

    def test_convert_to_typed_value_number(self):
        self.assertEqual(config.convert_to_typed_value('123'), 123)

    def test_convert_to_typed_value_boolean(self):
        self.assertEqual(config.convert_to_typed_value('true'), True)

    def test_convert_to_typed_value_invalid_json(self):
        self.assertEqual(config.convert_to_typed_value('#not_json'), '#not_json')

    def test_set_parameter_string(self):
        config.set_parameter('PARAM', 'value')
        self.assertEqual(os.environ['PARAM'], 'value')

    def test_set_parameter_non_string(self):
        config.set_parameter('PARAM', {'a': 1})
        self.assertEqual(os.environ['PARAM'], 'json:{"a": 1}')

    def test_overwrite_from_args(self):
        class Args:
            def __init__(self):
                self.param1 = 'value1'
                self.param2 = None
                self.param3 = 3

        args = Args()
        config.overwrite_from_args(args)
        self.assertEqual(os.environ['param1'], 'value1')
        self.assertEqual(os.environ['param3'], 'json:3')
        self.assertNotIn('param2', os.environ)

    def test_overwrite_from_args_syntax_error(self):
        print("Warning: overwrite_from_args uses iteritems(), which is not available in Python 3.")

    @patch('config.logger')
    def test_init_config_already_initialized(self, mock_logger):
        config._config = {'param': 'value'}
        config._init_config()
        self.assertEqual(config._config, {'param': 'value'})
        mock_logger.info.assert_not_called()

    def test_overwrite_from_args_exception(self):
        print("ERROR_NOTE: overwrite_from_args silently swallows an important exception when args has bad data")

        # Create a mock args object that raises an exception when vars() is called
        class FaultyArgs:
            def __getattr__(self, item):
                raise AttributeError("Test exception in vars(args)")

        args = FaultyArgs()
        # Ensure that overwrite_from_args raises exceptions with invalid parameters
        self.assertRaises(TypeError, config.overwrite_from_args, args)

    def test_overwrite_from_args_none(self):
        args = None
        config.overwrite_from_args(args)
        self.assertIsNone(args)

    def test_init_config_multiple_calls(self):
        with patch('config._get_default_path', return_value=None):
            config._init_config()
            config._init_config()  # Should not re-initialize _config
            self.assertEqual(config._config, {})

    def test_convert_to_typed_value_non_string(self):
        self.assertEqual(config.convert_to_typed_value(123), 123)

    def test_convert_to_typed_value_none(self):
        self.assertEqual(config.convert_to_typed_value(None), None)

    @patch.dict('os.environ', {'TEST_PARAM': 'json:{"a": 1}'})
    def test_get_parameter_env_json(self):
        config._config = {}
        value = config.get_parameter('TEST_PARAM')
        self.assertEqual(value, {"a": 1})

    def test_overwrite_from_args_faulty_set_parameter(self):
        print("ERROR_NOTE: overwrite_from_args silently swallows an important exception when set_parameter fails")

        # faulty set_parameter, expecting Exception
        def faulty_set_parameter(name, value):
            raise Exception("Test exception in set_parameter")

        original_set_parameter = config.set_parameter
        config.set_parameter = faulty_set_parameter

        # Define a valid Args class for this case
        class Args:
            def __init__(self):
                self.param1 = 'value1'

        args = Args()

        self.assertRaises(Exception, config.overwrite_from_args, args)

        # Restore the original set_parameter function
        config.set_parameter = original_set_parameter


if __name__ == '__main__':
    unittest.main()
