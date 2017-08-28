import unittest

from eobot.methods.get_mining_estimates import perform_request
from eobot.lib.eobot_config import get_config
from eobot.lib.eobot_request import EobotRequest
from eobot.tests.mock_server import MockServer


class GetMiningEstimatesTest(unittest.TestCase):
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

        estimates = perform_request(request=req.clone())

        self.assertIsInstance(estimates, dict)
        self.assertIn("MiningSHA-256", estimates.keys())

        self.assertIsInstance(estimates["MiningSHA-256"], float)
        self.assertEqual((1.0/6.0), estimates["MiningSHA-256"])

    def test_perform_request_with_config(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config("tgme").configure(456, "456@example.com", password="password", token=None)

        estimates = perform_request(config="tgme", request=req.clone())

        self.assertIsInstance(estimates, dict)
        self.assertIn("MiningSHA-256", estimates.keys())

        self.assertIsInstance(estimates["MiningSHA-256"], float)
        self.assertEqual((1.0/12.0), estimates["MiningSHA-256"])

    def test_perform_request_with_config_without_user_id(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config("tgme2").configure(email="456@example.com", password="password", token=None)

        estimates = perform_request(config=get_config("tgme2"), request=req.clone())

        self.assertIsInstance(estimates, dict)
        self.assertIn("MiningSHA-256", estimates.keys())

        self.assertIsInstance(estimates["MiningSHA-256"], float)
        self.assertEqual((1.0/12.0), estimates["MiningSHA-256"])
