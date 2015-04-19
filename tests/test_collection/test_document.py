# -*- encoding: UTF-8 -*-

from mongorest.collection import Collection, Document
from mongorest.testcase import TestCase

__all__ = [
    'TestDocument',
]


class TestDocument(TestCase):

    def test_init_sets_correct_collection(self):
        document = Document(Collection)

        self.assertEqual(document._cls, Collection)

    def test_init_sets_correct_fields(self):
        document = Document(Collection, {'test': 'test'})

        self.assertEqual(document._fields, {'test': 'test'})

