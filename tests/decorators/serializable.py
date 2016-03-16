# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from functools import wraps

from mongorest.decorators import serializable
from mongorest.testcase import TestCase


class TestSerializable(TestCase):

    def setUp(self):
        @serializable
        def test(*args, **kwargs):
            return {}

        self.func = test

    def test_serializable_creates_list_of_decorators_if_it_is_the_first(self):
        @serializable
        def test(*args, **kwargs):
            return {}

        self.assertIn('serializable', test.decorators)

    def test_serializable_appends_to_the_list_of_decorators_if_it_is_not_the_first(self):
        def test_decorator(wrapped):
            @wraps(wrapped)
            def wrapper(*args, **kwargs):
                return wrapped(*args, **kwargs)

            if hasattr(wrapped, 'decorators'):
                wrapper.decorators = wrapped.decorators
                wrapper.decorators.append('test_decorator')
            else:
                wrapper.decorators = ['test_decorator']

            return wrapper

        @serializable
        @test_decorator
        def test(*args, **kwargs):
            return {}

        self.assertIn('serializable', test.decorators)

    def test_serializable_serializes_result_if_keyword_serialize_is_true(self):
        self.assertEqual(self.func(serialize=True), '{}')

    def test_serializable_does_not_serialize_if_keyword_serialize_is_false(self):
        self.assertEqual(self.func(serialize=False), {})

    def test_serializable_does_not_serialize_if_keyword_serialize_is_not_passed(self):
        self.assertEqual(self.func(), {})
