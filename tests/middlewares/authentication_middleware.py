# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from os import environ
from pydoc import locate

from mongorest.resource import ListResourceMixin
from mongorest.settings import settings
from mongorest.testcase import TestCase
from mongorest.wrappers import Response
from mongorest.wsgi import WSGIDispatcher


class TestAuthenticationMiddleware(TestCase):

    def test_authentication_middleware_raises_value_error_if_session_store_is_not_sub_class_of_session_store(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.fixtures.middlewares_test_session_store_error_settings'

        self.test_client = self.client(
            WSGIDispatcher(resources=[ListResourceMixin]), Response
        )

        with self.assertRaises(ValueError):
            self.test_client.get('/')

        environ.pop('MONGOREST_SETTINGS_MODULE')

    def test_authentication_middleware_raises_value_error_if_auth_collection_is_not_sub_class_of_collection(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.fixtures.middlewares_test_auth_colelction_error_settings'

        self.test_client = self.client(
            WSGIDispatcher(resources=[ListResourceMixin]), Response
        )

        with self.assertRaises(ValueError):
            self.test_client.get('/')

        environ.pop('MONGOREST_SETTINGS_MODULE')

    def test_authentication_middleware_does_not_set_token_or_cookie_or_header_if_not_authorized(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.fixtures.middlewares_test_auth_settings'

        self.test_client = self.client(
            WSGIDispatcher(resources=[ListResourceMixin]), Response
        )

        response = self.test_client.get('/')

        self.assertNotIn('HTTP_AUTHORIZATION', response.headers)
        self.assertNotIn('Set-Cookie', response.headers)

        environ.pop('MONGOREST_SETTINGS_MODULE')

    def test_authentication_middleware_adds_authorization_header_to_response_authorized_with_token(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.fixtures.middlewares_test_auth_settings'

        class TestResource(ListResourceMixin):

            def list(self, request):
                request.environ['session']['test'] = 'test'
                request.environ['collection'] = 'collection'
                return Response()

        self.test_client = self.client(
            WSGIDispatcher(resources=[TestResource]), Response
        )

        session_store = locate(settings.SESSION_STORE)()
        session = session_store.new()
        session_store.save(session)

        response = self.test_client.get(
            '/', headers=[('Authorization', 'Token {0}'.format(session.sid))]
        )

        self.assertIn('HTTP_AUTHORIZATION', response.headers)
        self.assertEqual(
            response.headers.get('HTTP_AUTHORIZATION'), 'Token {0}'.format(session.sid)
        )

        environ.pop('MONGOREST_SETTINGS_MODULE')

    def test_authentication_middleware_adds_authorization_header_to_response_authorized_with_cookie(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.fixtures.middlewares_test_auth_settings'

        class TestResource(ListResourceMixin):

            def list(self, request):
                request.environ['session']['test'] = 'test'
                request.environ['collection'] = 'collection'
                return Response()

        self.test_client = self.client(
            WSGIDispatcher(resources=[TestResource]), Response
        )

        session_store = locate(settings.SESSION_STORE)()
        session = session_store.new()
        session_store.save(session)

        response = self.test_client.get(
            '/', headers=[('Cookie', 'session_id={0}'.format(session.sid))]
        )

        self.assertIn('HTTP_AUTHORIZATION', response.headers)
        self.assertEqual(
            response.headers.get('HTTP_AUTHORIZATION'), 'Token {0}'.format(session.sid)
        )

        environ.pop('MONGOREST_SETTINGS_MODULE')
