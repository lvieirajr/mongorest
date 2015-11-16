# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from os import environ

from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response

from mongorest.middlewares import CORSMiddleware
from mongorest.testcase import TestCase
from mongorest.wsgi import WSGIWrapper, WSGIDispatcher


class TestWSGIDispatcher(TestCase):

    def test_wsgi_dispatcher_init_returns_werkzeug_app_with_mounted_resources(self):
        class TestWSGIWrapper(WSGIWrapper):
            endpoint = 'test'
            url_map = Map([Rule('/', methods=['GET'], endpoint='test')])

            def test(self, request):
                return Response(status=999)

        app = WSGIDispatcher(resources=[TestWSGIWrapper])
        self.assertEqual(list(app.mounts.keys()), ['/test'])

    def test_wsgi_dispatcher_adds_middlewares_to_mounts(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.fixtures.wsgi_test_settings'

        class TestWSGIWrapper(WSGIWrapper):
            endpoint = 'test'
            url_map = Map([Rule('/', methods=['GET'], endpoint='test')])

            def test(self, request):
                return Response(status=999)

        app = WSGIDispatcher(resources=[TestWSGIWrapper])
        self.assertIsInstance(app.mounts['/test'], CORSMiddleware)

        environ.pop('MONGOREST_SETTINGS_MODULE')
