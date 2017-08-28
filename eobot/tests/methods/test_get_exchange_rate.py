import unittest

from eobot.methods.get_exchange_rate import perform_request
from eobot.lib.eobot_request import EobotRequest
from eobot.tests.mock_server import MockServer


class GetExchangeRateValueTest(unittest.TestCase):
    def setUp(self):
        self.server = MockServer()
        self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_perform_request_without_currency(self):
        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            perform_request()

    def test_perform_request_with_invalid_currency(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request(123)

    def test_perform_request_with_invalid_request(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request("EUR", request={})

    def test_perform_request(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        rate = perform_request("EUR", request=req.clone())

        self.assertIsInstance(rate, float)
        self.assertEqual(0.85, rate)
