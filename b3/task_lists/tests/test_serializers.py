from utils.test import SerializerTestCase

from .. import serializers


class ListSerializerTests(SerializerTestCase):
    serializer_class = serializers.ListSerializer

    def test_key(self):
        write_fields = {
            "name",
        }
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = {
            "id",
            "name",
        }
        self.assertReadFieldsSetEqual(read_fields)


class TaskSerializerTests(SerializerTestCase):
    serializer_class = serializers.TaskSerializer

    def test_key(self):
        write_fields = {
            "list_id",
            "description",
            "name",
        }
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = {
            "id",
            "list_id",
            "description",
            "name",
        }
        self.assertReadFieldsSetEqual(read_fields)


class TaskCreateSerializerTests(SerializerTestCase):
    serializer_class = serializers.TaskCreateSerializer

    def test_key(self):
        write_fields = {
            "description",
            "name",
        }
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = {
            "id",
            "list_id",
            "description",
            "name",
        }
        self.assertReadFieldsSetEqual(read_fields)
