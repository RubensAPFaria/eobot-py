import unittest

from eobot.lib.eobot_authentication import EobotReadonlyAuthentication, EobotWriteAuthentication
from eobot.lib.eobot_config import EobotConfig, get_config
from eobot.lib.eobot_errors import NoUserIdError, NoEmailError, NoPasswordOrTokenError


class EobotConfigTest(unittest.TestCase):
    def test_init(self):
        cfg = EobotConfig()

        self.assertIsNone(cfg._user_id)
        self.assertIsNone(cfg._email)
        self.assertIsNone(cfg._password)
        self.assertIsNone(cfg._token)

    def test_configure_with_valid_parameters(self):
        cfg = EobotConfig()

        self.assertIsNone(cfg._user_id)
        self.assertIsNone(cfg._email)
        self.assertIsNone(cfg._password)
        self.assertIsNone(cfg._token)

        cfg.configure(user_id=123, email="email", password="password", token="token")

        self.assertEqual(123, cfg._user_id)
        self.assertEqual("email", cfg._email)
        self.assertEqual("password", cfg._password)
        self.assertEqual("token", cfg._token)

    def test_configure_without_parameters(self):
        cfg = EobotConfig()
        cfg.configure(user_id=123, email="email", password="password", token="token")

        self.assertEqual(123, cfg._user_id)
        self.assertEqual("email", cfg._email)
        self.assertEqual("password", cfg._password)
        self.assertEqual("token", cfg._token)

        cfg.configure()

        self.assertEqual(123, cfg._user_id)
        self.assertEqual("email", cfg._email)
        self.assertEqual("password", cfg._password)
        self.assertEqual("token", cfg._token)

    def test_configure_with_valid_user_id(self):
        cfg = EobotConfig()
        cfg.configure(user_id=123)
        self.assertEqual(123, cfg._user_id)

    def test_configure_with_invalid_user_id(self):
        cfg = EobotConfig()

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            cfg.configure(user_id="123")

    def test_configure_with_none_user_id(self):
        cfg = EobotConfig()
        cfg.configure(user_id=123)
        self.assertEqual(123, cfg._user_id)

        cfg.configure(user_id=None)
        self.assertIsNone(cfg._user_id)

    def test_configure_with_valid_email(self):
        cfg = EobotConfig()
        cfg.configure(email="email")
        self.assertEqual("email", cfg._email)

    def test_configure_with_invalid_email(self):
        cfg = EobotConfig()

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            cfg.configure(email=123)

    def test_configure_with_none_email(self):
        cfg = EobotConfig()
        cfg.configure(email="email")
        self.assertEqual("email", cfg._email)

        cfg.configure(email=None)
        self.assertIsNone(cfg._email)

    def test_configure_with_valid_password(self):
        cfg = EobotConfig()
        cfg.configure(password="password")
        self.assertEqual("password", cfg._password)

    def test_configure_with_invalid_password(self):
        cfg = EobotConfig()

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            cfg.configure(password=123)

    def test_configure_with_none_password(self):
        cfg = EobotConfig()
        cfg.configure(password="password")
        self.assertEqual("password", cfg._password)

        cfg.configure(password=None)
        self.assertIsNone(cfg._password)

    def test_configure_with_valid_token(self):
        cfg = EobotConfig()
        cfg.configure(token="token")
        self.assertEqual("token", cfg._token)

    def test_configure_with_invalid_token(self):
        cfg = EobotConfig()

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            cfg.configure(token=123)

    def test_configure_with_none_token(self):
        cfg = EobotConfig()
        cfg.configure(token="token")
        self.assertEqual("token", cfg._token)

        cfg.configure(token=None)
        self.assertIsNone(cfg._token)

    def test_configure_set_single_parameter(self):
        cfg = EobotConfig()
        cfg.configure(user_id=123, email="email", password="password", token="token")

        self.assertEqual(123, cfg._user_id)
        self.assertEqual("email", cfg._email)
        self.assertEqual("password", cfg._password)
        self.assertEqual("token", cfg._token)

        cfg.configure(email="otheremail")

        # only email should be changed
        self.assertEqual(123, cfg._user_id)
        self.assertEqual("otheremail", cfg._email)
        self.assertEqual("password", cfg._password)
        self.assertEqual("token", cfg._token)

    def test_has_user_id(self):
        cfg = EobotConfig()
        self.assertFalse(cfg.has_user_id())

        cfg.configure(user_id=123)
        self.assertTrue(cfg.has_user_id())

        cfg.configure(user_id=None)
        self.assertFalse(cfg.has_user_id())

    def test_set_user_id_without_value(self):
        cfg = EobotConfig()

        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            cfg.set_user_id()

    def test_set_user_id_with_valid_value(self):
        cfg = EobotConfig()
        self.assertIsNone(cfg._user_id)
        cfg.set_user_id(123)
        self.assertEqual(123, cfg._user_id)

    def test_set_user_id_with_none_value(self):
        cfg = EobotConfig()
        cfg.configure(user_id=123)
        self.assertEqual(123, cfg._user_id)
        cfg.set_user_id(None)
        self.assertIsNone(cfg._user_id)

    def test_set_user_id_with_invalid_value(self):
        cfg = EobotConfig()

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            cfg.set_user_id("123")

    def test_get_user_id(self):
        cfg = EobotConfig()
        self.assertIsNone(cfg.get_user_id())

        cfg.set_user_id(123)
        self.assertEqual(123, cfg.get_user_id())

        cfg.set_user_id(None)
        self.assertIsNone(cfg.get_user_id())

    def test_has_email(self):
        cfg = EobotConfig()
        self.assertFalse(cfg.has_email())

        cfg.configure(email="email")
        self.assertTrue(cfg.has_email())

        cfg.configure(email=None)
        self.assertFalse(cfg.has_email())

    def test_set_email_without_value(self):
        cfg = EobotConfig()

        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            cfg.set_email()

    def test_set_email_with_valid_value(self):
        cfg = EobotConfig()
        self.assertIsNone(cfg._email)
        cfg.set_email("email")
        self.assertEqual("email", cfg._email)

    def test_set_email_with_none_value(self):
        cfg = EobotConfig()
        cfg.configure(email="email")
        self.assertEqual("email", cfg._email)
        cfg.set_email(None)
        self.assertIsNone(cfg._email)

    def test_set_email_with_invalid_value(self):
        cfg = EobotConfig()

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            cfg.set_email(123)

    def test_get_email(self):
        cfg = EobotConfig()
        self.assertIsNone(cfg.get_email())

        cfg.set_email("email")
        self.assertEqual("email", cfg.get_email())

        cfg.set_email(None)
        self.assertIsNone(cfg.get_email())

    def test_has_password(self):
        cfg = EobotConfig()
        self.assertFalse(cfg.has_password())

        cfg.configure(password="password")
        self.assertTrue(cfg.has_password())

        cfg.configure(password=None)
        self.assertFalse(cfg.has_password())

    def test_set_password_without_value(self):
        cfg = EobotConfig()

        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            cfg.set_password()

    def test_set_password_with_valid_value(self):
        cfg = EobotConfig()
        self.assertIsNone(cfg._password)
        cfg.set_password("password")
        self.assertEqual("password", cfg._password)

    def test_set_password_with_none_value(self):
        cfg = EobotConfig()
        cfg.configure(password="password")
        self.assertEqual("password", cfg._password)
        cfg.set_password(None)
        self.assertIsNone(cfg._password)

    def test_set_password_with_invalid_value(self):
        cfg = EobotConfig()

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            cfg.set_password(123)

    def test_get_password(self):
        cfg = EobotConfig()
        self.assertIsNone(cfg.get_password())

        cfg.set_password("password")
        self.assertEqual("password", cfg.get_password())

        cfg.set_password(None)
        self.assertIsNone(cfg.get_password())

    def test_has_token(self):
        cfg = EobotConfig()
        self.assertFalse(cfg.has_token())

        cfg.configure(token="token")
        self.assertTrue(cfg.has_token())

        cfg.configure(token=None)
        self.assertFalse(cfg.has_token())

    def test_set_token_without_value(self):
        cfg = EobotConfig()

        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            cfg.set_token()

    def test_set_token_with_valid_value(self):
        cfg = EobotConfig()
        self.assertIsNone(cfg._token)
        cfg.set_token("token")
        self.assertEqual("token", cfg._token)

    def test_set_token_with_none_value(self):
        cfg = EobotConfig()
        cfg.configure(token="token")
        self.assertEqual("token", cfg._token)
        cfg.set_token(None)
        self.assertIsNone(cfg._token)

    def test_set_token_with_invalid_value(self):
        cfg = EobotConfig()

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            cfg.set_token(123)

    def test_get_token(self):
        cfg = EobotConfig()
        self.assertIsNone(cfg.get_token())

        cfg.set_token("token")
        self.assertEqual("token", cfg.get_token())

        cfg.set_token(None)
        self.assertIsNone(cfg.get_token())

    def test_get_authentication_readonly_without_user_id(self):
        cfg = EobotConfig()

        with self.assertRaises(NoUserIdError):
            cfg.get_authentication(True)

    def test_get_authentication_readonly_with_user_id(self):
        cfg = EobotConfig()
        cfg.set_user_id(123)

        auth = cfg.get_authentication(True)
        self.assertIsInstance(auth, EobotReadonlyAuthentication)
        self.assertEqual(123, auth.user_id)

    def test_get_authentication_write_without_user_id(self):
        cfg = EobotConfig()

        with self.assertRaises(NoUserIdError):
            cfg.get_authentication(False)

    def test_get_authentication_write_with_user_id_without_email(self):
        cfg = EobotConfig()
        cfg.set_user_id(123)

        with self.assertRaises(NoEmailError):
            cfg.get_authentication(False)

    def test_get_authentication_write_with_user_id_with_email_without_password_or_token(self):
        cfg = EobotConfig()
        cfg.set_user_id(123)
        cfg.set_email("email")

        with self.assertRaises(NoPasswordOrTokenError):
            cfg.get_authentication(False)

    def test_get_authentication_write_with_user_id_with_email_with_password_without_token(self):
        cfg = EobotConfig()
        cfg.set_user_id(123)
        cfg.set_email("email")
        cfg.set_password("password")

        auth = cfg.get_authentication(False)
        self.assertIsInstance(auth, EobotWriteAuthentication)
        self.assertEqual(123, auth.user_id)
        self.assertEqual("email", auth.email)
        self.assertEqual("password", auth.password)

    def test_get_authentication_write_with_user_id_with_email_without_password_with_token(self):
        cfg = EobotConfig()
        cfg.set_user_id(123)
        cfg.set_email("email")
        cfg.set_token("token")

        auth = cfg.get_authentication(False)
        self.assertIsInstance(auth, EobotWriteAuthentication)
        self.assertEqual(123, auth.user_id)
        self.assertEqual("email", auth.email)
        self.assertEqual("token", auth.password)

    def test_get_authentication_write_with_user_id_with_email_with_password_with_token(self):
        cfg = EobotConfig()
        cfg.set_user_id(123)
        cfg.set_email("email")
        cfg.set_password("password")
        cfg.set_token("token")

        auth = cfg.get_authentication(False)
        self.assertIsInstance(auth, EobotWriteAuthentication)
        self.assertEqual(123, auth.user_id)
        self.assertEqual("email", auth.email)
        # token takes precedence over password, if available
        self.assertEqual("token", auth.password)


class GetConfigTest(unittest.TestCase):
    def test_global_config(self):
        cfg = get_config()
        self.assertIsInstance(cfg, EobotConfig)

        cfg.configure(user_id=123, email="email", password="password", token="token")
        self.assertTrue(get_config().has_user_id())
        self.assertTrue(get_config().has_email())
        self.assertTrue(get_config().has_password())
        self.assertTrue(get_config().has_token())

    def test_named_config_with_invalid_name(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            get_config(123)

    def test_named_config(self):
        # test order is unpredictable, make sure `test_global_config` runs first so the global config is filled
        self.test_global_config()
        self.assertTrue(get_config().has_user_id())
        self.assertTrue(get_config().has_email())
        self.assertTrue(get_config().has_password())
        self.assertTrue(get_config().has_token())

        cfg = get_config("named")
        self.assertIsInstance(cfg, EobotConfig)
        self.assertFalse(cfg.has_user_id())
        self.assertFalse(cfg.has_email())
        self.assertFalse(cfg.has_password())
        self.assertFalse(cfg.has_token())

        cfg.configure(user_id=456, email="email2", password="password2", token="token2")

        self.assertTrue(get_config("named").has_user_id())
        self.assertTrue(get_config("named").has_email())
        self.assertTrue(get_config("named").has_password())
        self.assertTrue(get_config("named").has_token())

        self.assertNotEqual(get_config().get_user_id(), get_config("named").get_user_id())
        self.assertNotEqual(get_config().get_email(), get_config("named").get_email())
        self.assertNotEqual(get_config().get_password(), get_config("named").get_password())
        self.assertNotEqual(get_config().get_token(), get_config("named").get_token())
