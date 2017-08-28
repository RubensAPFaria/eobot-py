import unittest

from eobot.methods.get_coin_value import perform_request
from eobot.lib.eobot_request import EobotRequest
from eobot.tests.mock_server import MockServer


class GetCoinValueTest(unittest.TestCase):
    def setUp(self):
        self.server = MockServer()
        self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_perform_request_without_coin(self):
        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            perform_request()

    def test_perform_request_with_invalid_coin(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request(123)

    def test_perform_request_with_invalid_request(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request("BTC", request={})

    def test_perform_request(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        value = perform_request("BTC", request=req.clone())

        self.assertIsInstance(value, float)
        self.assertEqual(100.0, value)
