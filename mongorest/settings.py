# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from inspect import getmembers
from os import environ, path

__all__ = [
    'settings',
]


DEFAULT = {
    'MONGODB': {
        'URI': '',
        'USERNAME': '',
        'PASSWORD': '',
        'HOSTS': ['localhost'],
        'PORTS': [27017],
        'DATABASE': 'mongorest',
        'OPTIONS': [],
    },
    'SERIALIZE': True,
}


class Settings(object):
    """
    Settings Class
    Will be responsible for loading the DEFAULT settings and USER settings
    Uses the environment variable MONGOREST_SETTINGS_MODULE to find where the
    Settings are store
    """

    _settings = DEFAULT

    def __init__(self):
        if 'MONGOREST_SETTINGS_MODULE' in environ:
            try:
                from importlib import import_module
                settings = import_module(environ['MONGOREST_SETTINGS_MODULE'])
            except:
                source = environ['MONGOREST_SETTINGS_MODULE'].replace(
                    '.', '/'
                ) + '.py'

                from imp import load_source
                settings = load_source('settings', path.abspath(source))

            self._settings = dict(
                self._settings,
                **dict(
                    (name, setting)
                    for (name, setting) in getmembers(settings)
                    if name.isupper()
                )
            )

    def __getattr__(self, attr):
        if attr not in self._settings:
            raise AttributeError('Invalid setting: \'{0}\''.format(attr))

        return self._settings.get(attr)


settings = Settings()
