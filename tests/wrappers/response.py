# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.testcase import TestCase
from mongorest.wrappers import Response


class TestResponse(TestCase):

    def test_json_returns_serialized_data(self):
        self.assertEqual(
            Response(response='{"1": 2, "test": [1, "2", null]}').json,
            {'1': 2, 'test': [1, '2', None]}
        )

    def test_json_returns_empty_dict_if_no_data(self):
        self.assertEqual(Response().json, {})
