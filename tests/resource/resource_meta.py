# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from werkzeug.routing import Rule

from mongorest.resource import Resource
from mongorest.testcase import TestCase
from mongorest.wrappers import Response


class TestResourceMeta(TestCase):

    def test_meta_adds_url_map_to_class_that_inherits_from_resource(self):
        class ResourceChild(Resource):
            rules = [Rule('/', methods=['GET'], endpoint='test')]

            def test(self, requet):
                return Response(status=999)

        for rule in ResourceChild.rules:
            self.assertTrue(rule in list(ResourceChild.url_map.iter_rules()))

    def test_meta_adds_url_map_to_class_that_inherits_from_resources_child_classes(self):
        class ResourceChild1(Resource):
            rules = [Rule('/', methods=['GET'], endpoint='test1')]

            def test1(self, requet):
                return Response(status=999)

        class ResourceChild2(Resource):
            rules = [Rule('/', methods=['GET'], endpoint='test2')]

            def test2(self, requet):
                return Response(status=999)

        class ResourceChildsChild(ResourceChild1, ResourceChild2):
            pass

        for rule in ResourceChild1.rules + ResourceChild2.rules:
            self.assertTrue(
                rule in list(ResourceChildsChild.url_map.iter_rules())
            )
