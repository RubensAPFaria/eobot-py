import unittest

from eobot.methods.manual_withdraw import perform_request
from eobot.methods.get_balances import perform_request as get_balances
from eobot.lib.eobot_config import get_config
from eobot.lib.eobot_request import EobotRequest
from eobot.tests.mock_server import MockServer


class ManualWithdrawTest(unittest.TestCase):
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

        self.assertEqual(0.2, get_balances(request=req.clone())["BTC"])

        result = perform_request("BTC", 0.1, "bitcoin-wallet", request=req.clone())
        self.assertTrue(result)

        self.assertEqual(0.1, get_balances(request=req.clone())["BTC"])

    def test_perform_request_with_config(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config("tmw").configure(456, "456@example.com", password="password", token=None)

        self.assertEqual(0.1, get_balances(config="tmw", request=req.clone())["BTC"])

        result = perform_request("BTC", 0.05, "wallet-bitcoin", config="tmw", request=req.clone())
        self.assertTrue(result)

        self.assertEqual(0.05, get_balances(config=get_config("tmw"), request=req.clone())["BTC"])

    def test_perform_request_with_config_without_user_id(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config("tmw2").configure(email="456@example.com", password="password", token=None)

        result = perform_request("BTC", 0.05, "wallet-bitcoin", config="tmw2", request=req.clone())
        self.assertTrue(result)

        self.assertEqual(0.05, get_balances(config=get_config("tmw2"), request=req.clone())["BTC"])
