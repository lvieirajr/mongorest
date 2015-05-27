# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.collection import Collection
from mongorest.middlewares import AuthenticationMiddleware

MIDDLEWARES = [AuthenticationMiddleware]
AUTH_COLLECTION = Collection
