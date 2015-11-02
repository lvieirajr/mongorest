# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import ValidationError
from mongorest.testcase import TestCase


class TestMongoRestError(TestCase):

    def test_validation_error_sets_correct_fields(self):
        self.assertEqual(
            ValidationError([1, 2, 3], 'collection', 'document'),
            {
                'error_code': 1,
                'error_type': 'ValidationError',
                'error_message': 'collection document validation failed.',
                'errors': [1, 2, 3],
                'collection': 'collection',
                'document': 'document',
            }
        )
