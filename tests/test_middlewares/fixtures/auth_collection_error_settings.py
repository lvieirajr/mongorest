# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from werkzeug.contrib.sessions import SessionStore

from mongorest.middlewares import AuthenticationMiddleware

MIDDLEWARES = [AuthenticationMiddleware]
SESSION_STORE = SessionStore
