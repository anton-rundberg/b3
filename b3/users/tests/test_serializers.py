from unittest.mock import Mock

from utils.test import SerializerTestCase

from .. import serializers
from . import factories


class AccessTokenSerializerTests(SerializerTestCase):
    serializer_class = serializers.AccessTokenSerializer

    def test_key(self):
        self.assertWriteFieldsSetEqual(set())
        read_fields = {
            "refresh",
            "access",
        }
        self.assertReadFieldsSetEqual(read_fields)


class RegistrationSerializerTests(SerializerTestCase):
    serializer_class = serializers.RegistrationSerializer

    def test_keys(self):
        write_fields = {
            "email",
            "first_name",
            "last_name",
            "password",
        }
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = {
            "email",
            "first_name",
            "last_name",
        }
        self.assertReadFieldsSetEqual(read_fields)

    def test_unique_case_insensitive_email(self):
        factories.UserFactory(email="aan-allein@example.com")
        data = {
            "email": "AAN-ALLEIN@example.com",
            "password": "Tai'SharMalkier",
            "first_name": "al'Lan",
            "last_name": "Mandragoran",
        }
        expected_errors = {"email": ["This field must be unique."]}
        self.assertSerializerErrors(data, expected_errors)


class ResetPasswordSerializerTests(SerializerTestCase):
    serializer_class = serializers.ResetPasswordSerializer

    def test_keys(self):
        write_fields = {
            "email",
        }
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = set()
        self.assertReadFieldsSetEqual(read_fields)


class ResetPasswordConfirmSerializerTests(SerializerTestCase):
    serializer_class = serializers.ResetPasswordConfirmSerializer

    def test_keys(self):
        write_fields = {
            "password",
            "token",
        }
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = set()
        self.assertReadFieldsSetEqual(read_fields)

    def test_invalid_token(self):
        data = {
            "password": "loremipsumdolorsitamet",
            "token": "invalid",
        }
        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors, {"token": [self.serializer_class.INVALID_TOKEN_ERROR]}
        )


class ChangePasswordSerializerTests(SerializerTestCase):
    serializer_class = serializers.ChangePasswordSerializer

    def test_keys(self):
        write_fields = {
            "current_password",
            "new_password",
        }
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = set()
        self.assertReadFieldsSetEqual(read_fields)

    def test_invalid_current_password(self):
        request = Mock()
        request.user = factories.UserFactory(password="the_password")
        data = {
            "current_password": "something_else",
            "new_password": "the_new_password",
        }
        context = {"request": request}
        serializer = self.serializer_class(data=data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors,
            {
                "current_password": [
                    self.serializer_class.CURRENT_PASSWORD_INCORRECT_ERROR
                ]
            },
        )


class UserMeSerializerTests(SerializerTestCase):
    serializer_class = serializers.UserMeSerializer

    def test_keys(self):
        write_fields = {
            "email",
            "first_name",
            "last_name",
        }
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = write_fields.union({"id", "is_staff"})
        self.assertReadFieldsSetEqual(read_fields)
