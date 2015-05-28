# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mock import patch

from mongorest.decorators import ensure_indexes, serializable
from mongorest.testcase import TestCase


class TestEnsureIndexes(TestCase):

    def test_ensure_indexes_appends_to_the_list_of_decorators(self):
        class Test(object):
            @classmethod
            def indexes(cls):
                pass

            @classmethod
            @serializable
            @ensure_indexes
            def test(cls, **kwargs):
                return None

        self.assertIn('ensure_indexes', Test.test.decorators)

    def test_ensure_indexes_calls_indexes_function_from_class(self):
        class Test(object):
            @classmethod
            def indexes(cls):
                pass

            @classmethod
            @ensure_indexes
            @serializable
            def test(cls, **kwargs):
                pass

        with patch.object(Test, 'indexes') as indexes:
            Test.test()

            self.assertEqual(indexes.call_count, 1)
