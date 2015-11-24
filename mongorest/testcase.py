# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from unittest import TestCase as BaseTestCase
from werkzeug.test import Client

from .database import db

__all__ = [
    'TestCase'
]


class TestCase(BaseTestCase):
    """
    Base TestCase class for users of the framework to use when testing.
    """

    def __init__(self, methodName='runtest'):
        super(TestCase, self).__init__(methodName)
        self.maxDiff = None

        self.db = db
        self.client = Client

        logging.disable(logging.CRITICAL)

    def __call__(self, *args, **kwargs):
        try:
            return super(TestCase, self).__call__(*args, **kwargs)
        finally:
            for collection in self.db.collection_names():
                if collection.startswith('system'):
                    continue

                self.db.drop_collection(collection)
