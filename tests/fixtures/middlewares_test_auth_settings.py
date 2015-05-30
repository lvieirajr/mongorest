# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

MIDDLEWARES = ['mongorest.middlewares.AuthenticationMiddleware']
SESSION_STORE = 'werkzeug.contrib.sessions.FilesystemSessionStore'
AUTH_COLLECTION = 'mongorest.collection.Collection'
