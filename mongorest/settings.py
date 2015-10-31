# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from inspect import getmembers
from pydoc import locate
from os import environ

__all__ = [
    'settings',
]


DEFAULT = {
    'AUTH_COLLECTION': '',
    'CORS': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,PATCH,DELETE,OPTIONS',
        'Access-Control-Allow-Headers': 'Accept,Accept-Encoding,Authorization,'
                                        'Content-Length,Content-Type,Origin,'
                                        'User-Agent,X-CSRFToken,'
                                        'X-Requested-With',
        'Access-Control-Allow-Credentials': 'true',
    },
    'MIDDLEWARES': [],
    'MONGODB': {
        'URI': '',
        'USERNAME': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'HOSTS': [],
        'PORT': 27017,
        'PORTS': [],
        'DATABASE': 'mongorest',
        'OPTIONS': [],
    },
    'SESSION_STORE': '',
}


class Settings(object):
    """
    Settings Class
    Will be responsible for loading the DEFAULT settings and USER settings
    Uses the environment variable MONGOREST_SETTINGS_MODULE to find where the
    Settings are store
    """

    def __getattr__(self, attr):
        self._settings = DEFAULT

        settings_module = environ.get('MONGOREST_SETTINGS_MODULE')
        if settings_module:
            loaded_settings = locate(settings_module)

            self._settings = dict(
                self._settings,
                **dict(
                    (name, setting)
                    for (name, setting) in getmembers(loaded_settings)
                    if name.isupper()
                )
            )

        if attr not in self._settings:
            raise AttributeError('Invalid setting: \'{0}\''.format(attr))

        return self._settings[attr]


settings = Settings()
