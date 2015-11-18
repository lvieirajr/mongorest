# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import UnknownFieldError
from mongorest.testcase import TestCase


class TestUnknownFieldError(TestCase):

    def test_unknown_field_sets_correct_fields(self):
        self.assertEqual(
            UnknownFieldError('collection', 'field'),
            {
                'error_code': 31,
                'error_type': 'UnknownFieldError',
                'error_message': 'Field \'field\' on collection '
                                 '\'collection\' is unknown.',
                'collection': 'collection',
                'field': 'field',
            }
        )
