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
    """
    Wrapper around Werkzeug Request object, provides easier access to data
    """

    def __init__(self, environ, populate_request=True, shallow=False):
        super(Request, self).__init__(environ, populate_request, shallow)

        args = {}
        for key, value in self.args.items():
            try:
                value = deserialize(value, object_pairs_hook=OrderedDict)
            finally:
                args[key] = value

        form = {}
        for key, value in self.form.items():
            try:
                value = deserialize(value, object_pairs_hook=OrderedDict)
            finally:
                form[key] = value

        self.args = args
        self.form = form
        self.json = deserialize(self.data.decode() or {})

        self.environ['wsgi.input'] = io.BytesIO(self.data)


class Response(WerkzeugResponse):
    """
    Wrapper around Werkzeug Response object, provides easier access to data
    """

    default_mimetype = 'application/json'

    @property
    def json(self):
        return deserialize(self.data.decode() or {})
