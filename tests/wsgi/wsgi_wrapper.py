# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from werkzeug.routing import Map, Rule

from mongorest.testcase import TestCase
from mongorest.wrappers import Response
from mongorest.wsgi import WSGIWrapper, WSGIDispatcher


class TestWSGIWrapper(TestCase):

    def test_wsgi_wrapper_sets_empty_endpoint(self):
        self.assertIsNotNone(WSGIWrapper.endpoint)

    def test_wsgi_wrapper_sets_empty_urls_list(self):
        self.assertIsInstance(WSGIWrapper.rules, list)

    def test_wsgi_wrapper_sets_empty_url_map(self):
        self.assertIsInstance(WSGIWrapper.url_map, Map)

    def test_wsgi_wrapper_executes_correct_view_if_url_exists_on_map(self):
        class WSGIWrapperTest(WSGIWrapper):
            url_map = Map([Rule('/', methods=['GET'], endpoint='test')])

            def test(self, request):
                return Response(status=999)

        app = WSGIDispatcher(resources=[WSGIWrapperTest])
        response = self.client(app, Response).get('/')

        self.assertEqual(response.status_code, 999)

    def test_wsgi_wrapper_returns_not_found_if_no_url_is_found_with_trailing_slash(self):
        class WSGIWrapperTest(WSGIWrapper):
            url_map = Map([Rule('/', methods=['GET'], endpoint='test')])

            def test(self, request):
                return Response(status=999)

        app = WSGIDispatcher(resources=[WSGIWrapperTest])
        response = self.client(app, Response).get('/test/')

        self.assertEqual(response.status_code, 404)

    def test_wsgi_wrapper_returns_not_found_if_no_url_is_found_without_trailing_slash(self):
        class WSGIWrapperTest(WSGIWrapper):
            url_map = Map([Rule('/', methods=['GET'], endpoint='test')])

            def test(self, request):
                return Response(status=999)

        app = WSGIDispatcher(resources=[WSGIWrapperTest])
        response = self.client(app, Response).get('/test')

        self.assertEqual(response.status_code, 404)

    def test_wsgi_wrapper_redirects_to_correct_url_if_30x_status_and_follow_redirects(self):
        class WSGIWrapperTest(WSGIWrapper):
            url_map = Map([Rule('/test/', methods=['GET'], endpoint='test')])

            def test(self, request):
                return Response(status=999)

        app = WSGIDispatcher(resources=[WSGIWrapperTest])
        response = self.client(app, Response).get('/test', follow_redirects=True)

        self.assertEqual(response.status_code, 999)
