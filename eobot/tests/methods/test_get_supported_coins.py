import unittest

from eobot.methods.get_supported_coins import perform_request
from eobot.lib.eobot_request import EobotRequest
from eobot.tests.mock_server import MockServer


class GetSupportedCoinsTest(unittest.TestCase):
    def setUp(self):
        self.server = MockServer()
        self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_perform_request_with_invalid_request(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request(request={})

    def test_perform_request(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        coins = perform_request(request=req.clone())

        self.assertIsInstance(coins, dict)
        self.assertIn("BTC", coins.keys())
        self.assertIn("ETH", coins.keys())

        self.assertIsInstance(coins["BTC"], dict)
        self.assertIsInstance(coins["ETH"], dict)

        self.assertIn("Price", coins["BTC"].keys())
        self.assertIn("Image", coins["BTC"].keys())
        self.assertIn("BigImage", coins["BTC"].keys())

        self.assertIn("Price", coins["ETH"].keys())
        self.assertIn("Image", coins["ETH"].keys())
        self.assertIn("BigImage", coins["ETH"].keys())

        self.assertIsInstance(coins["BTC"]["Price"], float)
        self.assertIsInstance(coins["BTC"]["Image"], basestring)
        self.assertIsInstance(coins["BTC"]["BigImage"], basestring)

        self.assertIsInstance(coins["ETH"]["Price"], float)
        self.assertIsInstance(coins["ETH"]["Image"], basestring)
        self.assertIsInstance(coins["ETH"]["BigImage"], basestring)

        self.assertEqual(100.0, coins["BTC"]["Price"])
        self.assertEqual("http://www.eobot.com/btc.png", coins["BTC"]["Image"])
        self.assertEqual("http://www.eobot.com/btcbig.png", coins["BTC"]["BigImage"])

        self.assertEqual(20.0, coins["ETH"]["Price"])
        self.assertEqual("http://www.eobot.com/eth.png", coins["ETH"]["Image"])
        self.assertEqual("http://www.eobot.com/ethbig.png", coins["ETH"]["BigImage"])
