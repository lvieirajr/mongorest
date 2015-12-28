# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import io
from collections import OrderedDict

from werkzeug.wrappers import (
    Request as WerkzeugRequest,
    Response as WerkzeugResponse,
)

from .utils import deserialize

__all__ = [
    'Request',
    'Response',
]


class Request(WerkzeugRequest):

    def __init__(self, environ, populate_request=True, shallow=False):
        super(Request, self).__init__(environ, populate_request, shallow)

        self.args = dict(
            (key, deserialize(value, object_pairs_hook=OrderedDict))
            for key, value in self.args.items()
        )
        self.form = dict(
            (key, deserialize(value))
            for key, value in self.form.items()
        )
        self.json = deserialize(self.data.decode() or {})

        self.environ['wsgi.input'] = io.BytesIO(self.data)


class Response(WerkzeugResponse):

    default_mimetype = 'application/json'

    @property
    def json(self):
        return deserialize(self.data.decode() or {})
