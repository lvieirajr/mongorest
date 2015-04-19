# -*- encoding: UTF-8 -*-

from pymongo import MongoClient

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
    db_settings = settings.DATABASE

    host = db_settings['HOST']
    port = db_settings['PORT']
    name = db_settings['NAME']
    user = db_settings['USER']
    password = db_settings['PASSWORD']

    database = MongoClient(host, port)[name]
    if not (user and password) or (user and password and
                                       database.authenticate(user, password)):
        return database

    return None


db = _get_db()
