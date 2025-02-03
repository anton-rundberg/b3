from unittest.mock import Mock

from utils.test import PermissionTestCase

from .. import permissions
from . import factories


class PasswordPermissionTests(PermissionTestCase):
    permission_class = permissions.PasswordPermission

    def setUp(self):
        self.user = factories.UserFactory()

    def test_success(self):
        password = "supersecret"
        self.user.set_password(password)
        request = Mock(user=self.user, data={"password": password})
        self.assertTrue(self.perm_call(request, None))

    def test_invalid_password(self):
        self.user.set_password("supersecret")
        request = Mock(user=self.user, data={"password": "somethingelese"})
        self.assertFalse(self.perm_call(request, None))

    def test_no_password(self):
        request = Mock(user=self.user, data={})
        self.assertFalse(self.perm_call(request, None))
