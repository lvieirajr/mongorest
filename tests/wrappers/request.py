# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import io
try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict

from mongorest.testcase import TestCase
from mongorest.wrappers import Request


class TestRequest(TestCase):

    def test_init_makes_args_become_a_dict_with_ordered_values_for_each_key(self):
        request = Request(
            environ={
                'QUERY_STRING': 'test={"a":2,"b":3}',
                'wsgi.input': io.BytesIO(b''),
            }
        )

        self.assertEqual(
            request.args,
            {'test': OrderedDict([('a', 2), ('b', 3)])}
        )
