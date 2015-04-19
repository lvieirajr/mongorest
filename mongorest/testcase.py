# -*- encoding: UTF-8 -*-

import logging
from unittest import TestCase as BaseTestCase

from .database import db


class TestCase(BaseTestCase):

    def __init__(self, methodName='runtest'):
        super(TestCase, self).__init__(methodName)

        self.maxDiff = None
        self.db = db

        logging.disable(logging.CRITICAL)

    def __call__(self, *args, **kwargs):
        try:
            return super(TestCase, self).__call__(*args, **kwargs)

        finally:
            for collection in self.db.collection_names():
                if collection.startswith('system'):
                    continue

                try:
                    self.db.drop_collection(collection)
                except:
                    pass
