# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.collection import Collection


class Account(Collection):

    def is_authorized(self):
        return True

    def authorized_methods(self):
        return ['GET']


AUTH_COLLECTION = 'tests.fixtures.decorators_test_settings.Account'
