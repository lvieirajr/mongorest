# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from .wsgi import WSGIDispatcher

__all__ = [
    'App',
]


class App(WSGIDispatcher):
    pass

