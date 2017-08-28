import unittest

from eobot.methods.get_mining_speed import perform_request
from eobot.lib.eobot_config import get_config
from eobot.lib.eobot_request import EobotRequest
from eobot.tests.mock_server import MockServer


class GetMiningSpeedTest(unittest.TestCase):
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

        speeds = perform_request(request=req.clone())

        self.assertIsInstance(speeds, dict)
        self.assertIn("MiningSHA-256", speeds.keys())

        self.assertIsInstance(speeds["MiningSHA-256"], float)
        self.assertEqual(10.0, speeds["MiningSHA-256"])

    def test_perform_request_with_config(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config("tgms").configure(456, "456@example.com", password="password", token=None)

        speeds = perform_request(config="tgms", request=req.clone())

        self.assertIsInstance(speeds, dict)
        self.assertIn("MiningSHA-256", speeds.keys())

        self.assertIsInstance(speeds["MiningSHA-256"], float)
        self.assertEqual(5.0, speeds["MiningSHA-256"])

    def test_perform_request_with_config_without_user_id(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config("tgms2").configure(email="456@example.com", password="password", token=None)

        speeds = perform_request(config=get_config("tgms2"), request=req.clone())

        self.assertIsInstance(speeds, dict)
        self.assertIn("MiningSHA-256", speeds.keys())

        self.assertIsInstance(speeds["MiningSHA-256"], float)
        self.assertEqual(5.0, speeds["MiningSHA-256"])
