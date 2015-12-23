# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import time

from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import AutoReconnect
from pymongo.mongo_client import MongoClient
from pymongo.mongo_replica_set_client import MongoReplicaSetClient
from pymongo.uri_parser import parse_uri


__all__ = [
    'db',
    'Executable',
    'MongoProxy'
]


EXECUTABLE_MONGO_METHODS = set(
    attr
    for obj in [Collection, Database, MongoClient, MongoReplicaSetClient]
    for attr in dir(obj)
    if not attr.startswith('_') and hasattr(getattr(obj, attr), '__call__')
)


class Executable(object):

    def __init__(self, method):
        self.method = method

    def __call__(self, *args, **kwargs):
        retries = 0

        while retries < 5:
            try:
                return self.method(*args, **kwargs)
            except AutoReconnect:
                time.sleep(pow(2, retries))

            retries += 1

        return self.method(*args, **kwargs)

    def __dir__(self):
        return dir(self.method)

    def __str__(self):
        return self.method.__str__()

    def __repr__(self):
        return self.method.__repr__()


class MongoProxy(object):

    def __init__(self, conn):
        self.conn = conn

    def __getitem__(self, key):
        item = self.conn[key]

        if hasattr(item, '__call__'):
            return MongoProxy(item)

        return item

    def __getattr__(self, key):
        attr = getattr(self.conn, key)

        if hasattr(attr, '__call__'):
            if key in EXECUTABLE_MONGO_METHODS:
                return Executable(attr)
            else:
                return MongoProxy(attr)

        return attr

    def __call__(self, *args, **kwargs):
        return self.conn(*args, **kwargs)

    def __dir__(self):
        return dir(self.conn)

    def __str__(self):
        return self.conn.__str__()

    def __repr__(self):
        return self.conn.__repr__()

    def __nonzero__(self):
        return True


def _get_db():
    """
    Returns the connection to the database using the settings.
    This function should not be called outside of this file.
    Use db instead.
    """
    from .settings import settings
    mongo = settings.MONGODB

    if 'URI' in mongo and mongo['URI']:
        uri = mongo['URI']
    else:
        uri = 'mongodb://'

        if all(mongo.get(key) for key in ('USERNAME', 'PASSWORD')):
            uri += '{0}:{1}@'.format(mongo['USERNAME'], mongo['PASSWORD'])

        if 'HOSTS' in mongo and mongo['HOSTS']:
            uri += ','.join(
                '{0}:{1}'.format(host, port)
                for (host, port) in zip(mongo['HOSTS'], mongo['PORTS']),
            )
        else:
            uri += '{0}:{1}'.format(mongo['HOST'], mongo.get('PORT', 27017))

        uri += '/' + mongo['DATABASE']

        if 'OPTIONS' in mongo and mongo['OPTIONS']:
            uri += '?{0}'.format('&'.join(mongo['OPTIONS']))

    return MongoProxy(MongoClient(uri))[parse_uri(uri)['database']]


db = _get_db()
