# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import time

from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
from pymongo.mongo_client import MongoClient
from pymongo.uri_parser import parse_uri

__all__ = [
    'db',
]


class ConnectionFailureProxy(object):

    def __init__(self, proxied):
        self.proxied = proxied
        self.logger = logging.getLogger(__name__)

    def __dir__(self):
        return dir(self.proxied)

    def __str__(self):
        return str(self.proxied)

    def __repr__(self):
        return repr(self.proxied)

    def __eq__(self, other):
        return self.proxied == other.proxied

    def __getitem__(self, key):
        item = self.proxied[key]

        if hasattr(item, '__call__'):
            item = ConnectionFailureProxy(item)

        return item

    def __getattr__(self, attr):
        attribute = getattr(self.proxied, attr)

        if hasattr(attribute, '__call__'):
            attribute = ConnectionFailureProxy(attribute)

        return attribute

    def __call__(self, *args, **kwargs):
        from .settings import settings

        retries = 0
        while retries < settings.RETRY_LIMIT:
            try:
                return self.proxied(*args, **kwargs)
            except ConnectionFailure:
                if settings.LINEAR_RETRIES:
                    sleep_time = settings.BASE_RETRY_TIME
                else:
                    sleep_time = pow(settings.BASE_RETRY_TIME, retries)

                retries += 1
                self.logger.warning(
                    'Retry nº %s in %s seconds.', retries, sleep_time
                )

                client, attempts = self.proxied, 0
                while attempts <= 3:
                    if isinstance(client, MongoClient):
                        client.close()
                        break
                    elif isinstance(client, Database):
                        client = client.client
                    elif isinstance(client, Collection):
                        client = client.database
                    else:
                        client = client.__self__

                    attempts += 1

                time.sleep(sleep_time)

        return self.proxied(*args, **kwargs)


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

    client = ConnectionFailureProxy(MongoClient(uri, connect=False))
    database = client[parse_uri(uri)['database']]

    return database


db = _get_db()
