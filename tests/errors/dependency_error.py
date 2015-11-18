# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import DependencyError
from mongorest.testcase import TestCase


class TestDependencyError(TestCase):

    def test_dependency_error_sets_correct_fields(self):
        self.assertEqual(
            DependencyError('collection', 'field', 'dependency'),
            {
                'error_code': 36,
                'error_type': 'DependencyError',
                'error_message': 'Field \'field\' on collection '
                                 '\'collection\' is required if field '
                                 '\'dependency\' is present.',
                'collection': 'collection',
                'field': 'field',
                'dependency': 'dependency',
            }
        )
