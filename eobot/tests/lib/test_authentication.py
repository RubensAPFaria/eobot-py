import unittest

from eobot.lib.eobot_authentication import EobotReadonlyAuthentication, EobotWriteAuthentication


class EobotReadOnlyAuthenticationTest(unittest.TestCase):
    def test_init_with_valid_user_id(self):
        auth = EobotReadonlyAuthentication(123)
        self.assertEqual(123, auth.user_id)

    def test_init_with_invalid_user_id(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            EobotReadonlyAuthentication("123")

    def test_init_with_none_user_id(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            EobotReadonlyAuthentication(None)

    def test_init_without_user_id(self):
        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            EobotReadonlyAuthentication()


class EobotWriteAuthenticationTest(unittest.TestCase):
    def test_init_with_valid_user_id_valid_email_valid_password(self):
        auth = EobotWriteAuthentication(123, "email", "password")
        self.assertEqual(123, auth.user_id)
        self.assertEqual("email", auth.email)
        self.assertEqual("password", auth.password)

    def test_init_with_valid_user_id_valid_email_invalid_password(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            EobotWriteAuthentication(123, "email", 456)

    def test_init_with_valid_user_id_valid_email_none_password(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            EobotWriteAuthentication(123, "email", None)

    def test_init_with_valid_user_id_valid_email_no_password(self):
        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            EobotWriteAuthentication(123, "email")

    def test_init_with_valid_user_id_invalid_email_valid_password(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            EobotWriteAuthentication(123, 456, "password")

    def test_init_with_valid_user_id_none_email_valid_password(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            EobotWriteAuthentication(123, None, "password")

    def test_init_with_valid_user_id_no_email_valid_password(self):
        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            EobotWriteAuthentication(123, password_or_token="password")

    def test_init_with_invalid_user_id_valid_email_valid_password(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            EobotWriteAuthentication("123", "email", "password")

    def test_init_with_none_user_id_valid_email_valid_password(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            EobotWriteAuthentication(None, "email", "password")

    def test_init_with_no_user_id_valid_email_valid_password(self):
        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            EobotWriteAuthentication(email="email", password_or_token="password")
