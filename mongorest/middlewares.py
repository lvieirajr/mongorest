# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from pydoc import locate
from werkzeug.contrib.sessions import SessionStore
from werkzeug.utils import dump_cookie, parse_cookie

from .collection import Collection
from .settings import settings
from .utils import deserialize

__all__ = [
    'AuthenticationMiddleware',
    'CORSMiddleware',
]


class AuthenticationMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        session_store = locate(settings.SESSION_STORE)

        if not session_store or not issubclass(session_store, SessionStore):
            raise ValueError(
                'SESSION_STORE must be a sub class of \'SessionStore\''
            )

        session_store = session_store()

        auth_collection = locate(settings.AUTH_COLLECTION)
        if not auth_collection or not issubclass(auth_collection, Collection):
            raise ValueError(
                'AUTH_COLLECTION must be a sub class of \'Collection\''
            )

        environ['session'] = session_store.new()

        session_id = environ.get('HTTP_AUTHORIZATION', '')
        if len(session_id.split('Token ')) == 2:
            session_id = session_id.split('Token ')[1]
            environ['session'] = session_store.get(session_id)
        else:
            cookies = environ.get('HTTP_COOKIE')

            if cookies:
                session_id = parse_cookie(cookies).get('session_id')

                if session_id:
                    environ['session'] = session_store.get(session_id)

        environ[auth_collection.__name__.lower()] = auth_collection.get({
            '_id': deserialize(
                environ['session'].get(auth_collection.__name__.lower(), '""')
            )
        })

        def authentication(status, headers, exc_info=None):
            if environ.get(auth_collection.__name__.lower()):
                headers.extend([
                    (
                        'Set-Cookie', dump_cookie(
                            'session_id', environ['session'].sid,
                            30 * 24 * 60 * 60,
                        )
                    ),
                    (
                        'HTTP_AUTHORIZATION', 'Token {0}'.format(
                            environ['session'].sid
                        )
                    ),
                ])

            return start_response(status, headers, exc_info)

        response = self.app(environ, authentication)

        if environ['session'].should_save:
            session_store.save(environ['session'])

        return response


class CORSMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def cors(status, headers, exc_info=None):
            headers.extend([
                (
                    'Access-Control-Allow-Origin',
                    settings.CORS['Access-Control-Allow-Origin']
                ),
                (
                    'Access-Control-Allow-Methods',
                    settings.CORS['Access-Control-Allow-Methods']
                ),
                (
                    'Access-Control-Allow-Headers',
                    settings.CORS['Access-Control-Allow-Headers']
                ),
                (
                    'Access-Control-Allow-Credentials',
                    settings.CORS['Access-Control-Allow-Credentials']
                )
            ])

            return start_response(status, headers, exc_info)

        if environ.get('REQUEST_METHOD') == 'OPTIONS':
            cors('200 OK', [('Content-Type', 'text/plain')])
            return [b'200 OK']

        return self.app(environ, cors)
