# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import UnauthorizedError
from mongorest.testcase import TestCase


class TestUnauthorizedError(TestCase):

    def test_unauthorized_error_sets_correct_fields(self):
        self.assertEqual(
            UnauthorizedError(),
            {
                'error_code': 1,
                'error_type': 'UnauthorizedError',
                'error_message': 'Unauthorized.',
            }
        )
