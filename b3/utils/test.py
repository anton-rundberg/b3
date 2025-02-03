import tempfile

from django.contrib.sessions.models import Session
from django.test import Client, TestCase
from django_otp import DEVICE_ID_SESSION_KEY
from PIL import Image
from rest_framework.fields import empty
from rest_framework.test import APITestCase

from users.models import User


def attach_2fa_to_user(client: Client, user: User) -> Session:
    # This function exists mostly for documentation purposes for testing with django-otp
    # Note that each call to client.session creates new session so we need to instantiate it for test
    device = user.staticdevice_set.create()
    session = client.session
    session[DEVICE_ID_SESSION_KEY] = device.persistent_id
    session.save()
    return session


def temporary_image():
    image = Image.new("RGB", (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(tmp_file, "jpeg")
    tmp_file.seek(
        0
    )  # important because after save(), the fp is already at the end of the file
    return tmp_file


class SerializerTestCase(TestCase):
    serializer_class = None

    def assertSerializerErrors(self, data, expected_errors, instance=None, **kwargs):
        serializer = self.serializer_class(instance=instance, data=data, **kwargs)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, expected_errors)

    def assertReadFieldsSetEqual(self, field_set, required_only=False):
        serializer = self.serializer_class()
        readable = set()
        for f in serializer._readable_fields:
            if required_only:
                if f.required:
                    readable.add(f.field_name)
            else:
                readable.add(f.field_name)

        self.assertSetEqual(readable, field_set)

    def assertWriteFieldsSetEqual(self, field_set, required_only=False):
        serializer = self.serializer_class()
        writable = set()
        for name, f in serializer.get_fields().items():
            if (not f.read_only) or (f.default is not empty):
                if required_only:
                    if f.required:
                        writable.add(name)
                else:
                    writable.add(name)

        self.assertSetEqual(writable, field_set)


class ViewTestCase(APITestCase):
    DEFAULT_ACTIONS = (
        "list",
        "retrieve",
        "create",
        "update",
        "partial_update",
        "destroy",
    )
    view_class = None

    @staticmethod
    def _perm_repr(klass):
        return klass.__class__

    def assertPermissions(self, expected, actions=DEFAULT_ACTIONS):
        view = self.view_class()
        expected_instances = [Klass() for Klass in expected]
        for action in actions:
            view.action = action
            self.assertSequenceEqual(
                list(map(self._perm_repr, view.get_permissions())),
                list(map(self._perm_repr, expected_instances)),
            )


class PermissionTestCase(TestCase):
    permission_class = None

    def perm_call(self, *args, **kwargs):
        return self.permission_class().has_permission(*args, **kwargs)
