# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from os import environ

from mongorest.testcase import TestCase
from mongorest.resource import ListResourceMixin
from mongorest.wrappers import Response
from mongorest.wsgi import WSGIDispatcher


class TestCORSMiddleware(TestCase):

    def setUp(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.fixtures.middlewares_test_cors_settings'

        self.test_client = self.client(
            WSGIDispatcher(resources=[ListResourceMixin]), Response
        )

    def test_cors_middleware_sets_correct_headers_on_options(self):
        response = self.test_client.options('/')

        self.assertIn('Access-Control-Allow-Origin', response.headers)
        self.assertIn('Access-Control-Allow-Methods', response.headers)
        self.assertIn('Access-Control-Allow-Headers', response.headers)
        self.assertIn('Access-Control-Allow-Credentials', response.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.data, b'200 OK')
        self.assertEqual(response.headers.get('Content-Type'), 'text/plain')

        environ.pop('MONGOREST_SETTINGS_MODULE')

    def test_cors_middleware_sets_correct_headers_on_other_methods(self):
        response = self.test_client.get('/')

        self.assertIn('Access-Control-Allow-Origin', response.headers)
        self.assertIn('Access-Control-Allow-Methods', response.headers)
        self.assertIn('Access-Control-Allow-Headers', response.headers)
        self.assertIn('Access-Control-Allow-Credentials', response.headers)

        environ.pop('MONGOREST_SETTINGS_MODULE')
