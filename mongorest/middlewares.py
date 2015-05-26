# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from .settings import settings

__all__ = [
    'CORSMiddleware',
]


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
            cors('200 Ok', [('Content-Type', 'text/plain')])
            return [b'200 Ok']

        return self.app(environ, cors)
