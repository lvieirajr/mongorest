# -*- encoding: UTF-8 -*-

from bson.dbref import DBRef
from bson.objectid import ObjectId
from calendar import timegm
from datetime import datetime
from uuid import uuid4

from mongorest.testcase import TestCase
from mongorest.utils import serialize

__all__ = [
    'TestSerialize',
]


class TestSerialize(TestCase):

    def test_serializing_a_string_returns_the_same_string(self):
        self.assertEqual(serialize('test'), 'test')

    def test_serializing_an_in_returns_the_same_int(self):
        self.assertEqual(serialize(1), 1)

    def test_serializing_a_float_returns_the_same_float(self):
        self.assertEqual(serialize(3.14), 3.14)

    def test_serializing_a_dict_returns_the_same_dict(self):
        self.assertEqual(serialize({'test': 'test'}), {'test': 'test'})

    def test_serializing_a_list_returns_the_same_list(self):
        self.assertEqual(serialize([1, 2, 3]), [1, 2, 3])

    def test_serializing_a_tuple_returns_the_same_tuple_as_a_list(self):
        self.assertEqual(serialize(tuple((1, 2, 3))), [1, 2, 3])

    def test_serializing_an_objectid_returns_a_dict_with_oid_as_key_and_the_str_as_value(self):
        oid = ObjectId()

        self.assertEqual(serialize(oid), {'$oid': str(oid)})

    def test_serializing_a_dbref_returns_a_dict_with_oid_as_key_and_the_str_as_value(self):
        dbref = DBRef('ref', 'id')

        self.assertEqual(serialize(dbref), {'$ref': 'ref', '$id': 'id'})

    def test_serializing_a_datetime_returns_a_dict_with_date_as_key_and_the_millis_as_value(self):
        date = datetime.now()
        milis = int(timegm(date.timetuple()) * 1000 + date.microsecond / 1000)

        self.assertEqual(serialize(date), {'$date': milis})

    def test_serializing_an_uuid_returns_a_dict_with_uuid_as_key_and_the_hex_as_value(self):
        uuid = uuid4()

        self.assertEqual(serialize(uuid), {'$uuid': uuid.hex})

