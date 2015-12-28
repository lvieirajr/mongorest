# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict

from werkzeug.test import create_environ

from mongorest.testcase import TestCase
from mongorest.wrappers import Request


class TestRequest(TestCase):

    def test_init_makes_args_become_a_dict_with_ordered_values_for_each_key(self):
        request1 = Request(
            create_environ(method='POST', query_string='test={"a":1,"b":2}')
        )

        request2 = Request(
            create_environ(method='POST', query_string='test={"b":2,"a":1}')
        )

        self.assertEqual(
            request1.args, {'test': OrderedDict([('a', 1), ('b', 2)])}
        )

        self.assertEqual(
            request2.args, {'test': OrderedDict([('b', 2), ('a', 1)])}
        )

    def test_init_makes_form_a_dict_with_decoded_and_deserialized_form_data(self):
        request = Request(create_environ(data={'a': 1, 'b': 2}))

        self.assertEqual(request.form, {'a': 1, 'b': 2})

    def test_init_makes_json_a_dict_with_decoded_and_deserialized_data(self):
        request = Request(create_environ(data='{"a":1,"b":2}'))

        self.assertEqual(request.json, {'a': 1, 'b': 2})
