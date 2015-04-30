# -*- encoding: UTF-8 -*-

from pymongo import MongoClient
from pymongo.uri_parser import parse_uri

from .settings import settings

__all__ = [
    'db',
]


def _get_db():
    """
    Returns the connection to the database using the settings.
    This function should not be called outside of this file.
    Use 'db' instead.
    """
    mongo = settings.MONGODB

    if 'URI' in mongo and mongo['URI']:
        uri = mongo['URI']
    else:
        uri = 'mongodb://'

        if all(mongo.get(key) for key in ('USERNAME', 'PASSWORD')):
            uri += '{}:{}@'.format(mongo['USERNAME'], mongo['PASSWORD'])

        uri += ','.join(
            '{}:{}'.format(host, port)
            for (host, port) in zip(mongo['HOSTS'], mongo['PORTS']),
        ) + '/' + mongo['DATABASE']

        if 'OPTIONS' in mongo and mongo['OPTIONS']:
            uri += '?{}'.format('&'.join(mongo['OPTIONS']))

    return MongoClient(uri)[parse_uri(uri)['database']]


db = _get_db()
