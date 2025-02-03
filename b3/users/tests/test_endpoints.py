from unittest.mock import patch

from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .. import models, serializers, views
from . import factories


class RegistrationViewTests(APITestCase):
    def test_create(self):
        self.assertFalse("_auth_user_id" in self.client.session)
        data = {
            "email": "aan-allein@example.com",
            "password": "Tai'SharMalkier",
            "first_name": "al'Lan",
            "last_name": "Mandragoran",
        }
        url = reverse("users:register")
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = models.User.objects.get(email=data["email"])
        self.assertTrue(user.check_password(data["password"]))

        # Check that user is logged in
        self.assertTrue("sessionid" in response.cookies)
        session_id = response.cookies["sessionid"].value
        self.assertEqual(session_id, self.client.session.session_key)
        self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))


class ResetPasswordTests(APITestCase):
    @patch("users.models.User.send_password_reset_email", autospec=True)
    def test_post(self, send_email_mock):
        user = factories.UserFactory(email="someone@example.com")
        data = {"email": user.email.upper()}
        url = reverse("users:reset-password")

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        send_email_mock.assert_called_once_with(user)


class ResetPasswordConfirmTests(APITestCase):
    def test_update(self):
        user = factories.UserFactory(email="someone@email.com", password="forgotten")
        data = {
            "password": "supersecret",
            "token": default_token_generator.make_token(user),
        }
        url = reverse("users:reset-password-confirm", kwargs={"user_id": str(user.pk)})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.check_password(data["password"]))


class ChangePasswordViewTests(APITestCase):
    def test_update(self):
        user = factories.UserFactory()
        current_password = "loremipsumdolorsitamet"
        new_password = "supersecret34134#"
        user.set_password(current_password)
        self.client.force_authenticate(user)
        url = reverse("users:change-password")
        data = {
            "current_password": current_password,
            "new_password": new_password,
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.check_password(new_password))


class UserMeViewTests(APITestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("users:user-me")

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        data = {
            "email": "newmail@example.com",
        }
        self.assertNotEqual(self.user.email, data["email"])
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, data["email"])

    def test_destroy(self):
        password = "bolag123"
        self.user.set_password(password)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(self.url, data={"password": password})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(models.User.DoesNotExist):
            self.user.refresh_from_db()


class CSRFCookieViewTests(APITestCase):
    def test_get(self):
        response = self.client.get(reverse("users:csrf"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("csrftoken" in response.cookies)
        self.assertEqual(response.cookies["csrftoken"]["samesite"], "Lax")
        self.assertEqual(response.cookies["csrftoken"]["httponly"], True)
        self.assertEqual(response.cookies["csrftoken"]["secure"], True)
        self.assertIn("csrf_token", response.json())


class LoginViewTests(APITestCase):
    def setUp(self):
        self.password = "mellon"
        self.user = factories.UserFactory(password=self.password)
        views.LoginView.throttle_classes = ()  # Disable throttling for tests

    def test_login_success(self):
        self.assertFalse("_auth_user_id" in self.client.session)
        data = {
            "email": self.user.email,
            "password": self.password,
        }
        url = reverse("users:login")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue("sessionid" in response.cookies)
        session_id = response.cookies["sessionid"].value
        self.assertEqual(session_id, self.client.session.session_key)
        self.assertEqual(self.client.session["_auth_user_id"], str(self.user.pk))

    def test_login_failure(self):
        data = {
            "email": self.user.email,
            "password": "wrongpassword",
        }
        url = reverse("users:login")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse("_auth_user_id" in self.client.session)
        self.assertFalse("sessionid" in response.cookies)
        self.assertEqual(
            response.data,
            {
                "non_field_errors": [
                    serializers.LoginSerializer.INCORRECT_EMAIL_OR_PASSWORD_MSG
                ]
            },
        )


class LogoutViewTests(APITestCase):
    def test_logout(self):
        user = factories.UserFactory()
        self.client.force_login(
            user
        )  # Use force_login instead of force_authenticate to create a session
        self.assertTrue("_auth_user_id" in self.client.session)
        url = reverse("users:logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.cookies["sessionid"].value, "")
        self.assertFalse("_auth_user_id" in self.client.session)
