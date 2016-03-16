# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from functools import wraps
from mock import Mock
from os import environ

from mongorest.decorators import login_required, serializable
from mongorest.testcase import TestCase
from mongorest.wrappers import Response


class TestLoginRequired(TestCase):

    def setUp(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.fixtures.login_required_test_settings'

        @login_required
        @serializable
        def test(self, request, **kwargs):
            return Response()

        self.func = test

    def test_login_required_creates_list_of_decorators_if_it_is_the_first(self):
        @login_required
        def test(self, request, **kwargs):
            return Response()

        self.assertIn('login_required', test.decorators)

    def test_login_required_appends_to_the_list_of_decorators_if_it_is_not_the_first(self):
        def test_decorator(wrapped):
            @wraps(wrapped)
            def wrapper(*args, **kwargs):
                return wrapped(*args, **kwargs)

            if hasattr(wrapped, 'decorators'):
                wrapper.decorators = wrapped.decorators
                wrapper.decorators.append('test_decorator')
            else:
                wrapper.decorators = ['test_decorator']

            return wrapper

        @login_required
        @test_decorator
        def test(*args, **kwargs):
            return {}

        self.assertIn('login_required', test.decorators)

    def test_login_required_returns_401_if_auth_collection_not_present(self):
        request = Mock(environ={})

        self.assertEqual(self.func(None, request).status_code, 401)

    def test_login_required_returns_401_if_auth_collection_is_none(self):
        request = Mock(environ={'account': None})

        self.assertEqual(self.func(None, request).status_code, 401)

    def test_login_required_returns_401_if_auth_collection_not_authorized(self):
        def is_authorized(request):
            return False

        account = Mock(is_authorized=is_authorized)
        request = Mock(environ={'account': account}, method='GET')

        self.assertEqual(self.func(None, request).status_code, 401)

    def test_login_required_returns_function_if_auth_collection_is_authorized(self):
        def is_authorized(request):
            return True

        account = Mock(is_authorized=is_authorized)
        request = Mock(environ={'account': account}, args={}, method='GET')

        self.assertEqual(self.func(None, request).status_code, 200)
