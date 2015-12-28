# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import time

from pymongo.errors import AutoReconnect
from pymongo.mongo_client import MongoClient
from pymongo.uri_parser import parse_uri

__all__ = [
    'db',
]


class AutoReconnectProxy(object):

    def __init__(self, proxied):
        self.proxied = proxied

    def __dir__(self):
        return dir(self.proxied)

    def __getitem__(self, key):
        item = self.proxied[key]

        if hasattr(item, '__call__'):
            item = AutoReconnectProxy(item)

        return item

    def __getattr__(self, attr):
        attribute = getattr(self.proxied, attr)

        if hasattr(attribute, '__call__'):
            attribute = AutoReconnectProxy(attribute)

        return attribute

    def __call__(self, *args, **kwargs):
        from .settings import settings

        retries = 0
        while retries < settings.RECONNECT_RETRIES:
            try:
                return self.proxied(*args, **kwargs)
            except AutoReconnect:
                time.sleep(pow(2, retries))

            retries += 1

        return self.proxied(*args, **kwargs)

    def __eq__(self, other):
        return self.proxied == other.proxied


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

    return AutoReconnectProxy(MongoClient(uri))[parse_uri(uri)['database']]


db = _get_db()
