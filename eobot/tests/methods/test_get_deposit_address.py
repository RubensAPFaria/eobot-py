import unittest

from eobot.methods.get_deposit_address import perform_request
from eobot.lib.eobot_config import get_config
from eobot.lib.eobot_request import EobotRequest
from eobot.tests.mock_server import MockServer

try:
    # noinspection PyShadowingBuiltins
    basestring = basestring
except NameError:
    # noinspection PyShadowingBuiltins
    basestring = (str, bytes)


class GetDepositAddressTest(unittest.TestCase):
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

    def test_perform_request_with_invalid_config(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request("BTC", config={})

    def test_perform_request_with_invalid_request(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request("BTC", request={})

    def test_perform_request(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config().configure(123, "123@example.com", password="password", token=None)

        wallet = perform_request("BTC", request=req.clone())

        self.assertIsInstance(wallet, basestring)
        self.assertEqual("bitcoin-wallet", wallet)

    def test_perform_request_with_config(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config("tgda").configure(456, "456@example.com", password="password", token=None)

        wallet = perform_request("ETH", config="tgda", request=req.clone())

        self.assertIsInstance(wallet, basestring)
        self.assertEqual("wallet-ethereum", wallet)

    def test_perform_request_with_config_without_user_id(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config("tgda2").configure(email="456@example.com", password="password", token=None)

        wallet = perform_request("BTC", config=get_config("tgda2"), request=req.clone())

        self.assertIsInstance(wallet, basestring)
        self.assertEqual("wallet-bitcoin", wallet)
