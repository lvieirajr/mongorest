# -*- encoding: UTF-8 -*-

from mongorest.collection import Collection
from mongorest.testcase import TestCase


class TestCollectionMeta(TestCase):

    def test_collection_meta_sets_correct_collection_and_meta(self):
        self.assertEqual(Collection.collection, self.db['collection'])
        self.assertEqual(Collection.meta, {'required': {}, 'optional': {}})
