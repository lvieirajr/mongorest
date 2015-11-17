# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import RegexMatchError
from mongorest.testcase import TestCase


class TestRegexMatchError(TestCase):

    def test_regex_match_error_sets_correct_fields(self):
        self.assertEqual(
            RegexMatchError('collection', 'field', 'regex'),
            {
                'error_code': 35,
                'error_type': 'RegexMatchError',
                'error_message': 'Value does not match the regex \'regex\' '
                                 'for field \'field\' of collection '
                                 '\'collection\'.',
                'collection': 'collection',
                'field': 'field',
                'regex': 'regex',
            }
        )
