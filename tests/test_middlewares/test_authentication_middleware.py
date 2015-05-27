# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from os import environ
from werkzeug.wrappers import Response

from mongorest.testcase import TestCase
from mongorest.resource import ListResourceMixin
from mongorest.wsgi import WSGIDispatcher


class TestAuthenticationMiddleware(TestCase):

    def setUp(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.test_middlewares.fixtures.authentication_settings'

        self.test_client = self.client(
            WSGIDispatcher([ListResourceMixin]), Response
        )

    def test_adds_authorization_header(self):
        response = self.test_client.get('/')

        self.assertIn('HTTP_AUTHORIZATION', response.headers)
        self.assertIn(response.headers.get('HTTP_AUTHORIZATION'), 'Token ')

        environ.pop('MONGOREST_SETTINGS_MODULE')
