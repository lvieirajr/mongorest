# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from inspect import getmembers
from os import environ, path

__all__ = [
    'settings',
]


DEFAULT = {
    'AUTH_COLLECTION': None,
    'CORS': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS, GET, HEAD, POST, PUT, '
                                        'PATCH, DELETE',
        'Access-Control-Allow-Headers': 'Authorization, Content-Length, '
                                        'Content-Type',
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
    'SESSION_STORE': None,
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
            try:
                from importlib import import_module
                loaded_settings = import_module(settings_module)
            except ImportError:
                source = '{0}.py'.format(settings_module.replace('.', '/'))

                from imp import load_source
                loaded_settings = load_source('settings', path.abspath(source))

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
