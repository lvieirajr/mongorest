# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import CoercionError
from mongorest.testcase import TestCase


class TestCoercionError(TestCase):

    def test_coercion_error_sets_correct_fields_if_passes_try(self):
        self.assertEqual(
            CoercionError('collection', 'field', 'coercion_type'),
            {
                'error_code': 38,
                'error_type': 'CoercionError',
                'error_message': 'Field \'field\' on collection '
                                 '\'collection\' could not be coerced into '
                                 'coercion_type.',
                'collection': 'collection',
                'field': 'field',
                'coercion_type': 'coercion_type',
            }
        )

    def test_coercion_error_sets_correct_fields_if_exception_is_raised(self):
        self.assertEqual(
            CoercionError('collection', 'field', 1),
            {
                'error_code': 38,
                'error_type': 'CoercionError',
                'error_message': 'Field \'field\' on collection '
                                 '\'collection\' could not be coerced into '
                                 '1.',
                'collection': 'collection',
                'field': 'field',
                'coercion_type': '1',
            }
        )
