# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

MIDDLEWARES = ['mongorest.middlewares.AuthenticationMiddleware']
AUTH_COLLECTION = 'mongorest.collection.Collection'
SESSION_STORE = 'mongorest.document.Document'
