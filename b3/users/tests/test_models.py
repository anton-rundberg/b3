from django.test import TestCase

from .. import models


class UserManagerTests(TestCase):
    data = {
        "email": "cAsIng@exaMple.com",
        "password": "Alohomora",
    }

    def test_create_user(self):
        self.assertFalse(models.User.objects.exists())
        user = models.User.objects.create_user(**self.data)
        self.assertTrue(models.User.objects.filter(id=user.id).exists())
        self.assertEqual(user.email, self.data["email"].lower())
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(self.data["password"]))

    def test_create_user_no_email(self):
        with self.assertRaises(ValueError) as e:
            models.User.objects.create_user(None)
        self.assertEqual(str(e.exception), "The Email must be set.")

    def test_create_superuser(self):
        self.assertFalse(models.User.objects.exists())
        user = models.User.objects.create_superuser(**self.data)
        self.assertTrue(models.User.objects.filter(id=user.id).exists())
        self.assertEqual(user.email, self.data["email"].lower())
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(self.data["password"]))

    def test_create_superuser_failure_is_staff_false(self):
        with self.assertRaises(ValueError) as e:
            models.User.objects.create_superuser(**{**self.data, "is_staff": False})
        self.assertEqual(str(e.exception), "Superuser must have is_staff=True.")

    def test_create_superuser_failure_is_superuser(self):
        with self.assertRaises(ValueError) as e:
            models.User.objects.create_superuser(**{**self.data, "is_superuser": False})
        self.assertEqual(str(e.exception), "Superuser must have is_superuser=True.")

    def test_normalize_email(self):
        self.assertEqual(
            models.User.objects.normalize_email(self.data["email"]),
            "casing@example.com",
        )

    def test_get_by_natural_key(self):
        user = models.User.objects.create_user(**self.data)
        user_natural = models.User.objects.get_by_natural_key(self.data["email"])
        self.assertEqual(user, user_natural)


class UserTests(TestCase):
    def test_to_string(self):
        user = models.User.objects.create_user(email="brakebills@nyu.com")
        self.assertEqual(str(user), "brakebills@nyu.com")

    def test_get_full_name(self):
        user = models.User.objects.create_user(
            email="brakebills@nyu.com",
            first_name="Quentin",
            last_name="Coldwater",
        )
        self.assertEqual(user.get_full_name(), "Quentin Coldwater")
