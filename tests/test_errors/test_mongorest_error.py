# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import MongoRestError
from mongorest.testcase import TestCase


class TestMongoRestError(TestCase):

    def test_mongorest_error_sets_correct_error_code_and_error_type_if_not_passed(self):
        self.assertEqual(
            MongoRestError(), {'error_code': -1, 'error_type': 'MongoRestError'}
        )

    def test_mongorest_error_sets_correct_error_code_and_error_type(self):
        self.assertEqual(
            MongoRestError(-2, 'TestError'),
            {'error_code': -2, 'error_type': 'TestError'}
        )
