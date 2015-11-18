# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import RequiredFieldError
from mongorest.testcase import TestCase


class TestRequiredFieldError(TestCase):

    def test_required_field_error_sets_correct_fields(self):
        self.assertEqual(
            RequiredFieldError('collection', 'field'),
            {
                'error_code': 23,
                'error_type': 'RequiredFieldError',
                'error_message': 'Field \'field\' on collection '
                                 '\'collection\' is required.',
                'collection': 'collection',
                'field': 'field',
            }
        )
