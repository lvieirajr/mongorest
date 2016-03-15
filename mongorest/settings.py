# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import copy
import inspect
import os
import pydoc

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
    'RETRY_LIMIT': 5,
    'BASE_RETRY_TIME': 2,
    'LINEAR_RETRIES': False,
    'SESSION_STORE': '',
}


class Settings(object):
    """
    Settings Class
    Will be responsible for loading the DEFAULT settings and USER settings
    Uses the environment variable MONGOREST_SETTINGS_MODULE to find where the
    Settings are store
    """
    _settings = copy.deepcopy(DEFAULT)
    _settings_module = None

    def __getattr__(self, name):
        settings_module = os.environ.get('MONGOREST_SETTINGS_MODULE')

        if not settings_module:
            self._settings_module = None
            self._settings = copy.deepcopy(DEFAULT)
        if settings_module and self._settings_module != settings_module:
            self._settings_module = settings_module

            self._settings = dict(
                self._settings, **dict(
                    (name, setting) for (name, setting) in inspect.getmembers(
                        pydoc.locate(settings_module)
                    ) if name.isupper()
                )
             )

        try:
            return self._settings[name]
        except KeyError:
            raise AttributeError('Invalid setting: \'{0}\''.format(name))


settings = Settings()
