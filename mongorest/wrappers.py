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

        args = {}
        for key, value in self.args.items():
            try:
                args[key] = deserialize(value, object_pairs_hook=OrderedDict)
            except Exception:
                args[key] = value

        form = {}
        for key, value in self.form.items():
            try:
                form[key] = deserialize(value, object_pairs_hook=OrderedDict)
            except Exception:
                form[key] = value

        self.args = args
        self.form = form
        self.json = deserialize(self.data.decode() or {})

        self.environ['wsgi.input'] = io.BytesIO(self.data)


class Response(WerkzeugResponse):

    default_mimetype = 'application/json'

    @property
    def json(self):
        return deserialize(self.data.decode() or {})
