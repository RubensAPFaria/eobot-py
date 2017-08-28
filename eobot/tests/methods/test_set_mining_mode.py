import unittest

from eobot.methods.set_mining_mode import perform_request
from eobot.methods.get_mining_mode import perform_request as get_mining_mode
from eobot.lib.eobot_config import get_config
from eobot.lib.eobot_request import EobotRequest
from eobot.tests.mock_server import MockServer


class SetMiningModeTest(unittest.TestCase):
    def setUp(self):
        self.server = MockServer()
        self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_perform_request_without_arguments(self):
        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            perform_request()

    def test_perform_request_with_invalid_mode(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request(123)

    def test_perform_request_with_invalid_config(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request("ETH", config={})

    def test_perform_request_with_invalid_request(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            perform_request("ETH", request={})

    def test_perform_request(self):
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config().configure(123, "123@example.com", password="password", token=None)

        mode_before = get_mining_mode(request=req.clone())
        self.assertEqual("BTC", mode_before)

        result = perform_request("ETH", request=req.clone())
        self.assertTrue(result)

        mode_after = get_mining_mode(request=req.clone())
        self.assertEqual("ETH", mode_after)

    def test_perform_request_with_config(self):
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config("tsmm").configure(456, "456@example.com", password="password", token=None)

        mode_before = get_mining_mode(config="tsmm", request=req.clone())
        self.assertEqual("ETH", mode_before)

        result = perform_request("BTC", config="tsmm", request=req.clone())
        self.assertTrue(result)

        mode_after = get_mining_mode(config="tsmm", request=req.clone())
        self.assertEqual("BTC", mode_after)

    def test_perform_request_with_config_without_user_id(self):
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config("tsmm2").configure(email="456@example.com", password="password", token=None)

        result = perform_request("BTC", config=get_config("tsmm2"), request=req.clone())
        self.assertTrue(result)
