# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from bson.dbref import DBRef
from bson.objectid import ObjectId
from datetime import datetime
from uuid import UUID

from mongorest.testcase import TestCase
from mongorest.utils import deserialize


class TestDeserialize(TestCase):

    def test_deserializing_a_serialized_string_returns_the_same_string(self):
        self.assertEqual(deserialize('"test"'), 'test')

    def test_deserializing_a_serialized_int_returns_the_same_int(self):
        self.assertEqual(deserialize('1'), 1)

    def test_deserializing_a_serialized_float_returns_the_same_float(self):
        self.assertEqual(deserialize('3.14'), 3.14)

    def test_deserializing_a_serialized_dict_returns_the_same_dict(self):
        self.assertEqual(deserialize('{"test": "test"}'), {'test': 'test'})

    def test_deserializing_a_serialized_list_returns_the_same_list(self):
        self.assertEqual(deserialize('[1, 2, 3]'), [1, 2, 3])

    def test_deserializing_an_object_id_string_returns_an_object_id(self):
        oid = ObjectId('0123456789ab0123456789ab')

        self.assertEqual(deserialize('0123456789ab0123456789ab'), oid)

    def test_deserializing_a_serialized_object_id_returns_the_original_object_id(self):
        oid = ObjectId('0123456789ab0123456789ab')

        self.assertEqual(
            deserialize('{"$oid": "0123456789ab0123456789ab"}'), oid
        )

    def test_deserializing_a_serialized_dbref_returns_the_original_dbref(self):
        dbref = DBRef('ref', 'id')

        self.assertEqual(deserialize('{"$ref": "ref", "$id": "id"}'), dbref)

    def test_deserializing_a_serialized_datetime_returns_the_original_datetime_with_tz(self):
        date = datetime(2015, 1, 1, 1, 1, 1)

        deserialized_date = deserialize('{"$date": 1420074061000}')
        self.assertEqual(
            deserialized_date.utctimetuple(), date.utctimetuple()
        )

    def test_deserializing_a_serialized_uuid_returns_the_original_uuid(self):
        uuid = UUID('149ead99640043a2874ad83e00c559c2')

        self.assertEqual(
            deserialize('{"$uuid": "149ead99640043a2874ad83e00c559c2"}'), uuid
        )

    def test_deserialize_serializes_and_deserializes_back_if_to_deserialize_is_already_a_json(self):
        self.assertEqual(deserialize({'123': 123}), {'123': 123})
