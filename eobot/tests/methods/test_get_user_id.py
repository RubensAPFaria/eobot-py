import unittest

from eobot.lib.eobot_errors import NoEmailError, NoPasswordOrTokenError
from eobot.methods.get_user_id import perform_request
from eobot.lib.eobot_config import get_config
from eobot.lib.eobot_request import EobotRequest
from eobot.tests.mock_server import MockServer


class GetUserIdTest(unittest.TestCase):
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

    def test_perform_request_with_config_without_email(self):
        get_config("tgui1").configure(user_id=None, email=None, password=None, token=None)

        with self.assertRaises(NoEmailError):
            perform_request(config=get_config("tgui1"))

    def test_perform_request_with_config_without_password_or_token(self):
        get_config("tgui2").configure(user_id=None, email="123@example.com", password=None, token=None)

        with self.assertRaises(NoPasswordOrTokenError):
            perform_request(config=get_config("tgui2"))

    def test_perform_request_with_valid_config(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config().configure(None, "123@example.com", password="password", token=None)

        user_id = perform_request(request=req.clone())

        self.assertIsInstance(user_id, int)
        self.assertEqual(123, user_id)

    def test_perform_request_with_config(self):
        MockServer.reset()
        req = EobotRequest()
        req.set_base_url('http://localhost:{0}/api.test'.format(self.server.port))

        get_config("tgui3").configure(456, "456@example.com", password="password", token=None)

        user_id = perform_request(config="tgui3", request=req.clone())

        self.assertIsInstance(user_id, int)
        self.assertEqual(456, user_id)
