# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mock import patch

from mongorest.decorators import ensure_indexes
from mongorest.testcase import TestCase


class TestEnsureIndexes(TestCase):

    def test_ensure_indexes_calls_indexes_function_from_class(self):
        class Test(object):
            @classmethod
            def indexes(cls):
                pass

            @classmethod
            @ensure_indexes
            def test(cls):
                pass

        with patch.object(Test, 'indexes') as indexes:
            Test.test()

            self.assertEqual(indexes.call_count, 1)
