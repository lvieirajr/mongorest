# -*- encoding: UTF-8 -*-

from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.routing import Map
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import DispatcherMiddleware

from .utils import serialize


__all__ = [
    'WSGIWrapper',
    'WSGIDispatcher',
]


class WSGIWrapper(object):

    rules = []
    url_map = Map()

    def __call__(self, environ, start_response):
        adapter = self.url_map.bind_to_environ(environ)

        try:
            endpoint, values = adapter.match()
            response = getattr(self, endpoint)(Request(environ), **values)
        except HTTPException as exc:
            if hasattr(exc, 'get_response'):
                response = exc.get_response(environ)
            else:
                response = Response(
                    serialize({'error': exc.description}),
                    content_type='application/json',
                    status=exc.code
                )

        return response(environ, start_response)


class WSGIDispatcher(DispatcherMiddleware):

    def __init__(self, resources):
        super(WSGIDispatcher, self).__init__(
            NotFound(),
            {
                '/{}'.format(resource.endpoint): resource()
                for resource in resources
            }
        )
