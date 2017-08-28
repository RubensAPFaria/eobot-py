import unittest

from eobot.methods.get_exchange_estimate import perform_request
from eobot.lib.eobot_request import EobotRequest
from eobot.tests.mock_server import MockServer


class GetExchangeEstimateTest(unittest.TestCase):
    def setUp(self):
        self.server = MockServer()
        self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_perform_request_without_arguments(self):
        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            perform_request()

    def test_perform_request_without_from_coin(self):
        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            perform_request(amount=1.0, to_coin="ETH")

    def test_perform_request_without_to_coin(self):
        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            perform_request(from_coin="BTC", amount=1.0)

    def test_perform_request_without_amount(self):
        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            perform_request(from_coin="BTC", to_coin="ETH")

    def test_perform_request_with_invalid_from_coin(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request(123, "ETH", 1.0)

    def test_perform_request_with_invalid_to_coin(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request("BTC", 123, 1.0)

    def test_perform_request_with_invalid_amount(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request("BTC", "ETH", "one")

    def test_perform_request_with_invalid_request(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request("BTC", "ETH", 1.0, request={})

    def test_perform_request(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        estimate = perform_request("BTC", "ETH", 1.0, request=req.clone())

        self.assertIsInstance(estimate, float)
        self.assertEqual(5.0, estimate)
