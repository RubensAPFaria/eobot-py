import unittest

from eobot.lib.eobot_request import EobotRequest
from eobot import __version__
from eobot.tests.mock_server import MockServer


class EobotRequestTest(unittest.TestCase):
    def test_default_values(self):
        req = EobotRequest()

        self.assertEqual(30.0, req._timeout)
        self.assertTrue(req._validate_ssl)
        self.assertEqual(
            'RickDenHaan-Eobot/{0} (+http://github.com/rickdenhaan/eobot-py)'.format(__version__),
            req._user_agent
        )
        self.assertEqual('https://www.eobot.com/api.aspx', req._base_url)
        self.assertIsInstance(req._parameters, dict)
        self.assertEqual(0, len(req._parameters))

    def test_set_timeout_without_value(self):
        req = EobotRequest()

        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            req.set_timeout()

    def test_set_timeout_with_invalid_value(self):
        req = EobotRequest()

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            req.set_timeout("10")

    def test_set_timeout_with_int(self):
        req = EobotRequest()
        req.set_timeout(10)
        self.assertIsInstance(req._timeout, float)
        self.assertEqual(10.0, req._timeout)

    def test_set_timeout_with_float(self):
        req = EobotRequest()
        req.set_timeout(10.5)
        self.assertEqual(10.5, req._timeout)

    def test_get_timeout(self):
        req = EobotRequest()
        self.assertEqual(30.0, req.get_timeout())
        req.set_timeout(10)
        self.assertEqual(10.0, req.get_timeout())

    def test_set_validate_ssl_without_value(self):
        req = EobotRequest()

        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            req.set_validate_ssl()

    def test_set_validate_ssl_with_invalid_value(self):
        req = EobotRequest()

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            req.set_validate_ssl(1)

    def test_set_validate_ssl_with_bool(self):
        req = EobotRequest()
        req.set_validate_ssl(False)
        self.assertEqual(False, req._validate_ssl)

    def test_get_validate_ssl(self):
        req = EobotRequest()
        self.assertEqual(True, req.get_validate_ssl())
        req.set_validate_ssl(False)
        self.assertEqual(False, req.get_validate_ssl())

    def test_set_user_agent_without_value(self):
        req = EobotRequest()

        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            req.set_user_agent()

    def test_set_user_agent_with_invalid_value(self):
        req = EobotRequest()

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            req.set_user_agent(123)

    def test_set_user_agent_with_str(self):
        req = EobotRequest()
        req.set_user_agent("UserAgent")
        self.assertEqual("UserAgent", req._user_agent)

    def test_get_user_agent(self):
        req = EobotRequest()
        self.assertEqual(
            'RickDenHaan-Eobot/{0} (+http://github.com/rickdenhaan/eobot-py)'.format(__version__),
            req.get_user_agent()
        )
        req.set_user_agent("UserAgent")
        self.assertEqual("UserAgent", req.get_user_agent())

    def test_set_base_url_without_value(self):
        req = EobotRequest()

        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            req.set_base_url()

    def test_set_base_url_with_invalid_value(self):
        req = EobotRequest()

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            req.set_base_url(123)

    def test_set_base_url_with_str(self):
        req = EobotRequest()
        req.set_base_url("url")
        self.assertEqual("url", req._base_url)

    def test_get_base_url(self):
        req = EobotRequest()
        self.assertEqual('https://www.eobot.com/api.aspx', req.get_base_url())
        req.set_base_url("url")
        self.assertEqual("url", req.get_base_url())

    def test_set_parameters_without_value(self):
        req = EobotRequest()

        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            req.set_parameters()

    def test_set_parameters_with_invalid_value(self):
        req = EobotRequest()

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            req.set_parameters(123)

    def test_set_parameters_with_dict(self):
        req = EobotRequest()
        req.set_parameters({"key": "value"})
        self.assertEqual(1, len(req._parameters))
        self.assertIn("key", req._parameters.keys())
        self.assertEqual("value", req._parameters["key"])

    def test_set_parameter_without_key_without_value(self):
        req = EobotRequest()

        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            req.set_parameter()

    def test_set_parameter_without_key_with_value(self):
        req = EobotRequest()

        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            req.set_parameter(value="value")

    def test_set_parameter_with_key_without_value(self):
        req = EobotRequest()

        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            req.set_parameter("key")

    def test_set_parameters_with_invalid_key(self):
        req = EobotRequest()

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            req.set_parameter(123, 456)

    def test_set_parameter_with_valid_arguments(self):
        req = EobotRequest()
        req.set_parameter("key", "value")
        self.assertEqual(1, len(req._parameters))
        self.assertIn("key", req._parameters.keys())
        self.assertEqual("value", req._parameters["key"])

    def test_get_parameters(self):
        req = EobotRequest()
        self.assertIsInstance(req.get_parameters(), dict)
        self.assertEqual(0, len(req.get_parameters()))
        req.set_parameters({"key": "value"})
        self.assertEqual(1, len(req.get_parameters()))
        self.assertIn("key", req.get_parameters().keys())
        self.assertEqual("value", req.get_parameters()["key"])
        req.set_parameter("key_2", "value_2")
        self.assertEqual(2, len(req.get_parameters()))
        self.assertIn("key", req.get_parameters().keys())
        self.assertEqual("value", req.get_parameters()["key"])
        self.assertIn("key_2", req.get_parameters().keys())
        self.assertEqual("value_2", req.get_parameters()["key_2"])

    def test_perform_request(self):
        server = MockServer()
        server.start()

        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(server.port))
        req.set_parameter("coin", "BTC")
        response = req.perform_request()

        server.stop()

        self.assertIsInstance(response, dict)
        self.assertIn("BTC", response)
        self.assertIsInstance(response["BTC"], float)
        self.assertEqual(100.0, response["BTC"])

    def test_perform_request_with_error(self):
        server = MockServer()
        server.start()

        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(server.port))
        req.set_parameter("nosuch", "page")

        with self.assertRaises(RuntimeError):
            req.perform_request()

        server.stop()
