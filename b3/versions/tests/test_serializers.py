from utils.test import SerializerTestCase

from .. import serializers


class VersionSerializerTests(SerializerTestCase):
    serializer_class = serializers.VersionSerializer

    def test_key(self):
        write_fields = set()
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = {
            "minimum_version",
        }
        self.assertReadFieldsSetEqual(read_fields)
