# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from werkzeug.contrib.sessions import FilesystemSessionStore

from mongorest.collection import Collection
from mongorest.middlewares import AuthenticationMiddleware

MIDDLEWARES = [AuthenticationMiddleware]
SESSION_STORE = FilesystemSessionStore
AUTH_COLLECTION = Collection
