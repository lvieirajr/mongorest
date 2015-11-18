# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import ValueDependencyError
from mongorest.testcase import TestCase


class TestValueDependencyError(TestCase):

    def test_value_dependency_error_sets_correct_fields(self):
        self.assertEqual(
            ValueDependencyError(
                'collection', 'field', 'dependency', 'dependency_values'
            ),
            {
                'error_code': 46,
                'error_type': 'ValueDependencyError',
                'error_message': 'Field \'field\' on collection '
                                 '\'collection\' is required to have values '
                                 '\'dependency_values\' if field '
                                 '\'dependency\' is present.',
                'collection': 'collection',
                'field': 'field',
                'dependency': 'dependency',
                'dependency_values': 'dependency_values',
            }
        )
