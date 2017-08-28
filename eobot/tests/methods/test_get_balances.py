import unittest

from eobot.methods.get_balances import perform_request
from eobot.lib.eobot_config import get_config
from eobot.lib.eobot_request import EobotRequest
from eobot.tests.mock_server import MockServer


class GetBalancesTest(unittest.TestCase):
    def setUp(self):
        self.server = MockServer()
        self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_perform_request_with_invalid_config(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request(config={})

    def test_perform_request_with_invalid_request(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request(request={})

    def test_perform_request(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config().configure(123, "123@example.com", password="password", token=None)

        balances = perform_request(request=req.clone())

        self.assertIsInstance(balances, dict)
        self.assertEqual(3, len(balances))
        self.assertIn("BTC", balances.keys())
        self.assertIn("ETH", balances.keys())
        self.assertIn("Total", balances.keys())

        self.assertEqual(0.2, balances["BTC"])
        self.assertEqual(2.5, balances["ETH"])
        self.assertEqual(70.0, balances["Total"])

    def test_perform_request_with_config(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config("tgb").configure(456, "456@example.com", password="password", token=None)

        balances = perform_request(config="tgb", request=req.clone())

        self.assertIsInstance(balances, dict)
        self.assertEqual(3, len(balances))
        self.assertIn("BTC", balances.keys())
        self.assertIn("ETH", balances.keys())
        self.assertIn("Total", balances.keys())

        self.assertEqual(0.1, balances["BTC"])
        self.assertEqual(2.0, balances["ETH"])
        self.assertEqual(50.0, balances["Total"])

    def test_perform_request_with_config_without_user_id(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config("tgb2").configure(email="456@example.com", password="password", token=None)

        balances = perform_request(config=get_config("tgb2"), request=req.clone())

        self.assertIsInstance(balances, dict)
        self.assertEqual(3, len(balances))
        self.assertIn("BTC", balances.keys())
        self.assertIn("ETH", balances.keys())
        self.assertIn("Total", balances.keys())

        self.assertEqual(0.1, balances["BTC"])
        self.assertEqual(2.0, balances["ETH"])
        self.assertEqual(50.0, balances["Total"])
