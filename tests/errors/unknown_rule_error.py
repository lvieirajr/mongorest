# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import UnknownRuleError
from mongorest.testcase import TestCase


class TestUnknownRuleError(TestCase):

    def test_unknown_rule_error_sets_correct_fields(self):
        self.assertEqual(
            UnknownRuleError('collection', 'field', 'rule'),
            {
                'error_code': 13,
                'error_type': 'UnknownRuleError',
                'error_message': 'Unknown rule \'rule\' for field \'field\' '
                                 'on collection \'collection\'.',
                'collection': 'collection',
                'field': 'field',
                'rule': 'rule',
            }
        )
