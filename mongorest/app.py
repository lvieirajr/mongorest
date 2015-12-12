# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from .collection import Collection
from .database import db
from .settings import settings
from .wsgi import WSGIDispatcher

__all__ = [
    'App',
]


class App(object):
    pass

