from unittest.mock import ANY

from rest_framework import status
from rest_framework.reverse import reverse

from users.tests.factories import UserFactory
from utils.test import ViewTestCase

from .. import models
from . import factories


class ListViewSetTests(ViewTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.other_user = UserFactory()

        cls.list = factories.ListFactory(user=cls.user)
        cls.list_2 = factories.ListFactory(user=cls.user)

        cls.task_1 = factories.TaskFactory(list=cls.list)
        cls.task_2 = factories.TaskFactory(list=cls.list)

        cls.other_list = factories.ListFactory(user=cls.other_user)

        cls.detail_url = reverse(
            "task_list:list-detail",
            kwargs={
                "pk": cls.list.pk,
            },
        )
        cls.list_url = reverse("task_list:list-list")

        cls.other_detail_url = reverse(
            "task_list:list-detail",
            kwargs={
                "pk": cls.other_list.pk,
            },
        )

    def setUp(self):
        self.client.force_authenticate(self.user)

    def test_retrieve(self):
        with self.assertNumQueries(1):
            response = self.client.get(self.detail_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["id"], str(self.list.pk))

    def test_retrieve_other(self):
        response = self.client.get(self.other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list(self):
        with self.assertNumQueries(2):
            response = self.client.get(self.list_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["id"], str(self.list_2.pk))
        self.assertEqual(response.data["results"][1]["id"], str(self.list.pk))

    def test_patch_change_name(self):
        data = {
            "name": self.list.name + "adding something",
        }
        with self.assertNumQueries(2):
            response = self.client.patch(self.detail_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["id"], str(self.list.pk))
        self.assertEqual(response.data["name"], data["name"])

        self.list.refresh_from_db()
        self.assertEqual(self.list.name, data["name"])

    def test_patch_other(self):
        data = {
            "name": self.list.name + "adding something",
        }
        with self.assertNumQueries(1):
            response = self.client.patch(self.other_detail_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.other_list.refresh_from_db()
        self.assertNotEqual(self.other_list, data["name"])

    def test_delete(self):
        with self.assertNumQueries(3):
            response = self.client.delete(self.detail_url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(models.List.DoesNotExist):
            self.list.refresh_from_db()

        task_count = models.Task.objects.filter(
            pk__in=[self.task_1.pk, self.task_2.pk]
        ).count()
        self.assertEqual(task_count, 0)

    def test_delete_other(self):
        with self.assertNumQueries(1):
            response = self.client.delete(self.other_detail_url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        list_exists = models.List.objects.filter(pk=self.list.pk).exists()
        self.assertTrue(list_exists)

    def test_create(self):
        my_list_count = models.List.objects.filter(user=self.user).count()

        data = {
            "name": "new list",
        }

        with self.assertNumQueries(1):
            response = self.client.post(self.list_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["id"], ANY)
        self.assertEqual(response.data["name"], data["name"])

        my_new_list_count = models.List.objects.filter(user=self.user).count()
        self.assertEqual(my_new_list_count, my_list_count + 1)


class TaskViewTests(ViewTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.other_user = UserFactory()

        cls.list = factories.ListFactory(user=cls.user)
        cls.list_2 = factories.ListFactory(user=cls.user)

        cls.task_1 = factories.TaskFactory(list=cls.list)
        cls.task_2 = factories.TaskFactory(list=cls.list)

        cls.other_list = factories.ListFactory(user=cls.other_user)

        cls.other_task = factories.TaskFactory(list=cls.other_list)

        cls.detail_url = reverse(
            "task_list:task-detail",
            kwargs={
                "pk": cls.list.pk,
                "task_id": cls.task_1.pk,
            },
        )
        cls.list_url = reverse(
            "task_list:task-list",
            kwargs={
                "pk": cls.list.pk,
            },
        )

        cls.other_detail_url = reverse(
            "task_list:task-detail",
            kwargs={
                "pk": cls.other_list.pk,
                "task_id": cls.other_task.pk,
            },
        )

    def setUp(self):
        self.client.force_authenticate(self.user)

    def test_retrieve(self):
        with self.assertNumQueries(1):
            response = self.client.get(self.detail_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["id"], str(self.task_1.pk))

    def test_retrieve_other(self):
        response = self.client.get(self.other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list(self):
        with self.assertNumQueries(2):
            response = self.client.get(self.list_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["id"], str(self.task_2.pk))
        self.assertEqual(response.data["results"][1]["id"], str(self.task_1.pk))

    def test_patch_change_metadata(self):
        data = {
            "name": self.task_1.name + "new",
            "description": self.task_1.description + "looong",
        }
        with self.assertNumQueries(3):
            response = self.client.patch(self.detail_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.task_1.refresh_from_db()
        self.assertEqual(self.task_1.name, data["name"])
        self.assertEqual(self.task_1.description, data["description"])

    def test_patch_add_my_task_to_my_other_list(self):
        data = {
            "list_id": self.list_2,
        }
        with self.assertNumQueries(1):
            response = self.client.patch(self.detail_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.task_1.refresh_from_db()
        self.assertEqual(self.task_1.list_id, self.list.pk)

    def test_patch_add_my_task_to_other_list(self):
        data = {
            "list_id": self.other_list,
        }
        with self.assertNumQueries(1):
            response = self.client.patch(self.detail_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.task_1.refresh_from_db()
        self.assertEqual(self.task_1.list_id, self.list.pk)

    def test_delete(self):
        self.assertEqual(self.list.task_set.count(), 2)

        with self.assertNumQueries(2):
            response = self.client.delete(self.detail_url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(models.Task.DoesNotExist):
            self.task_1.refresh_from_db()

        self.assertEqual(self.list.task_set.count(), 1)

    def test_delete_other(self):
        self.assertEqual(self.other_list.task_set.count(), 1)

        with self.assertNumQueries(1):
            response = self.client.delete(self.other_detail_url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(self.other_list.task_set.count(), 1)

    def test_create(self):
        my_list_task_count = self.list.task_set.count()

        data = {"name": "my cool new task"}
        with self.assertNumQueries(1):
            response = self.client.post(self.list_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["id"], ANY)

        my_new_list_task_count = self.list.task_set.count()
        self.assertEqual(my_new_list_task_count, my_list_task_count + 1)
