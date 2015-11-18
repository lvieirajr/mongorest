# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import ReadOnlyFieldError
from mongorest.testcase import TestCase


class TestReadOnlyFieldError(TestCase):

    def test_read_only_field_error_sets_correct_fields(self):
        self.assertEqual(
            ReadOnlyFieldError('collection', 'field'),
            {
                'error_code': 33,
                'error_type': 'ReadOnlyFieldError',
                'error_message': 'Field \'field\' on collection '
                                 '\'collection\' is read only.',
                'collection': 'collection',
                'field': 'field',
            }
        )
