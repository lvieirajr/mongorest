# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import UnknownTypeError
from mongorest.testcase import TestCase


class TestUnknownTypeError(TestCase):

    def test_unknown_type_error_sets_correct_fields(self):
        self.assertEqual(
            UnknownTypeError('collection', 'field', 'type'),
            {
                'error_code': 15,
                'error_type': 'UnknownTypeError',
                'error_message': 'Type \'type\' for field \'field\' was not '
                                 'recognized on the validation schema for '
                                 'collection \'collection\'.',
                'collection': 'collection',
                'field': 'field',
                'type': 'type',
            }
        )
