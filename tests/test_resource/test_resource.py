# -*- encoding: UTF-8 -*-

from werkzeug.routing import Rule
from werkzeug.wrappers import Response

from mongorest.collection import Collection
from mongorest.resource import Resource
from mongorest.testcase import TestCase


class TestResource(TestCase):

    def test_resource_meta_returns_rules_and_url_map_of_base_resources(self):
        class TestResource1(Resource):
            rules = [Rule('/', methods=['GET'], endpoint='test1')]

            def test1(self, request):
                return Response(status=999)

        class TestResource2(Resource):
            rules = [Rule('/', methods=['POST'], endpoint='test2')]

            def test2(self, request):
                return Response(status=999)

        class TestResource(TestResource1, TestResource2):
            pass

        self.assertEqual(len(TestResource.rules), 2)
        self.assertEqual(
            TestResource.rules,
            TestResource1.rules + TestResource2.rules
        )
        for rule in TestResource.url_map.iter_rules():
            self.assertIn(rule, TestResource1.rules + TestResource2.rules)

    def test_resource_meta_also_returns_base_collection_and_endpoint(self):
        self.assertEqual(Resource.collection, Collection)
        self.assertEqual(Resource.endpoint, '/')

    def test_resource_meta_call_sets_rules_if_no_rules_from_bases(self):
        class TestResource1(Resource):
            rules = [Rule('/', methods=['GET'], endpoint='test1')]

            def test1(self, request):
                return Response(status=999)

        self.assertEqual(len(list(TestResource1().url_map.iter_rules())), 1)
