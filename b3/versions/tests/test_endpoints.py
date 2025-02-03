from rest_framework import status
from rest_framework.reverse import reverse

from utils.test import ViewTestCase

from . import factories


class VersionViewTests(ViewTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("versions:version")

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        factories.VersionFactory(minimum_version="1.0.0")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["minimum_version"], "1.0.0")

        factories.VersionFactory(minimum_version="1.1.0")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["minimum_version"], "1.1.0")
