# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.collection import Collection
from mongorest.testcase import TestCase
from mongorest.validator import Validator


class TestCollectionMeta(TestCase):

    def test_collection_meta_sets_correct_collection_and_schema_and_allow_unknown_and_validator(self):
        self.assertEqual(Collection.collection, self.db['collection'])
        self.assertEqual(Collection.schema, {})
        self.assertTrue(Collection.allow_unknown)
        self.assertIsInstance(Collection.validator, Validator)

    def test_get_attr_raises_exception_if_can_not_find_attr(self):
        with self.assertRaises(AttributeError):
            Collection._()
