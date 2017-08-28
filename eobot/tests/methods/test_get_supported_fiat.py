import unittest

from eobot.methods.get_supported_fiat import perform_request
from eobot.lib.eobot_request import EobotRequest
from eobot.tests.mock_server import MockServer


class GetSupportedFiatTest(unittest.TestCase):
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

        fiat = perform_request(request=req.clone())

        self.assertIsInstance(fiat, dict)
        self.assertIn("USD", fiat.keys())
        self.assertIn("EUR", fiat.keys())

        self.assertIsInstance(fiat["USD"], dict)
        self.assertIsInstance(fiat["EUR"], dict)

        self.assertIn("Price", fiat["USD"].keys())
        self.assertIn("Price", fiat["EUR"].keys())

        self.assertIsInstance(fiat["USD"]["Price"], float)
        self.assertIsInstance(fiat["EUR"]["Price"], float)

        self.assertEqual(1.0, fiat["USD"]["Price"])
        self.assertEqual(0.85, fiat["EUR"]["Price"])
