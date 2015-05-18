# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.decorators import serializable
from mongorest.testcase import TestCase


class TestSerializable(TestCase):

    def setUp(self):
        class Test(object):
            @serializable
            def test(cls, **kwargs):
                return kwargs

        self.test = Test()

    def test_serializable_serializes_result_if_keyword_serialize_is_true(self):
        self.assertEqual(self.test.test(serialize=True), '{}')

    def test_serializable_does_not_serialize_if_keyword_serialize_is_false(self):
        self.assertEqual(self.test.test(serialize=False), {})

    def test_serializable_does_not_serialize_if_keyword_serialize_is_not_passed(self):
        self.assertEqual(self.test.test(), {})
