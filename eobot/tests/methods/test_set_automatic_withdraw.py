import unittest

from eobot.methods.set_automatic_withdraw import perform_request
from eobot.lib.eobot_config import get_config
from eobot.lib.eobot_request import EobotRequest
from eobot.tests.mock_server import MockServer


class SetAutomaticWithdrawTest(unittest.TestCase):
    def setUp(self):
        self.server = MockServer()
        self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_perform_request_without_arguments(self):
        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            perform_request()

    def test_perform_request_with_invalid_coin(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request(123, 0.1, "bitcoin-wallet")

    def test_perform_request_with_invalid_amount(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request("BTC", "0.1", "bitcoin-wallet")

    def test_perform_request_with_invalid_wallet(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request("BTC", 0.1, 456)

    def test_perform_request_with_invalid_config(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request("BTC", 0.1, "bitcoin-wallet", config={})

    def test_perform_request_with_invalid_request(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request("BTC", 0.11, "bitcoin-wallet", request={})

    def test_perform_request(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config().configure(123, "123@example.com", password="password", token=None)

        result = perform_request("BTC", 0.1, "bitcoin-wallet", request=req.clone())
        self.assertTrue(result)

    def test_perform_request_with_config(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config("tsaw").configure(456, "456@example.com", password="password", token=None)

        result = perform_request("BTC", 0.05, "wallet-bitcoin", config="tsaw", request=req.clone())
        self.assertTrue(result)

    def test_perform_request_with_config_without_user_id(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config("tsaw2").configure(email="456@example.com", password="password", token=None)

        result = perform_request("BTC", 0.05, "wallet-bitcoin", config="tsaw2", request=req.clone())
        self.assertTrue(result)
