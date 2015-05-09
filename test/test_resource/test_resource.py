# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.collection import Collection
from mongorest.resource import Resource
from mongorest.testcase import TestCase


class TestResource(TestCase):

    def test_resource_sets_collection(self):
        self.assertEqual(Resource.collection, Collection)
