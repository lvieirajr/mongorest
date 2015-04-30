# -*- encoding: UTF-8 -*-

from importlib import import_module
from inspect import getmembers
from os import environ

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
            settings = import_module(environ['MONGOREST_SETTINGS_MODULE'])

            self._settings = dict(
                self._settings,
                **{
                    name: setting
                    for (name, setting) in getmembers(settings)
                    if name.isupper()
                }
            )

    def __getattr__(self, attr):
        if attr not in self._settings:
            raise AttributeError('Invalid setting: \'{}\''.format(attr))

        return self._settings.get(attr)


settings = Settings()
