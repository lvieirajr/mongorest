# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import PyMongoError
from mongorest.testcase import TestCase


class TestPyMongoError(TestCase):

    def test_pymongo_error_sets_correct_fields(self):
        self.assertEqual(
            PyMongoError('error_message', 'test', 'collection', 'document'),
            {
                'error_code': 0,
                'error_type': 'PyMongoError',
                'error_message': 'error_message',
                'operation': 'test',
                'collection': 'collection',
                'document': 'document',
            }
        )
