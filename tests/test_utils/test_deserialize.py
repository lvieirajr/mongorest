# -*- encoding: UTF-8 -*-

from bson.dbref import DBRef
from bson.objectid import ObjectId
from calendar import timegm
from datetime import datetime
from uuid import uuid4

from mongorest.testcase import TestCase
from mongorest.utils import deserialize

__all__ = [
    'TestDeserialize',
]


class TestDeserialize(TestCase):

    def test_deserializing_a_string_returns_the_same_string(self):
        self.assertEqual(deserialize('test'), 'test')

    def test_deserializing_an_in_returns_the_same_int(self):
        self.assertEqual(deserialize(1), 1)

    def test_deserializing_a_float_returns_the_same_float(self):
        self.assertEqual(deserialize(3.14), 3.14)

    def test_deserializing_a_dict_returns_the_same_dict(self):
        self.assertEqual(deserialize({'test': 'test'}), {'test': 'test'})

    def test_deserializing_a_list_returns_the_same_list(self):
        self.assertEqual(deserialize([1, 2, 3]), [1, 2, 3])

    def test_deserializing_a_tuple_returns_the_same_tuple_as_a_list(self):
        self.assertEqual(deserialize(tuple((1, 2, 3))), [1, 2, 3])

    def test_deserializing_a_serialized_object_id_returns_the_original_object_id(self):
        oid = ObjectId()

        self.assertEqual(deserialize({'$oid': str(oid)}), oid)

    def test_deserializing_a_serialized_dbref_returns_the_original_dbref(self):
        dbref = DBRef('ref', 'id')

        self.assertEqual(deserialize({'$ref': 'ref', '$id': 'id'}), dbref)

    def test_deserializing_a_serialized_datetime_returns_the_original_datetime_with_tz(self):
        date = datetime.now()
        milis = int(timegm(date.timetuple()) * 1000 + date.microsecond / 1000)

        deserialized_date = deserialize({'$date': milis})
        self.assertEqual(
            deserialized_date.utctimetuple(), date.utctimetuple()
        )

    def test_deserializing_a_serialized_uuid_returns_the_original_uuid(self):
        uuid = uuid4()

        self.assertEqual(deserialize({'$uuid': uuid.hex}), uuid)
