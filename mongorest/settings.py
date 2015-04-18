# -*- encoding: UTF-8 -*-

__all__ = [
    'settings',
]


DEFAULT = {
    'DATABASE': {
        'HOST': 'localhost',
        'PORT': 27017,
        'NAME': 'mongorest',
        'USER': '',
        'PASSWORD': '',
    }
}


class Settings(object):

    def __init__(self, settings=None):
        self.settings = dict(DEFAULT, **settings)

    def __getattr__(self, attr):
        if attr not in self.settings.keys():
            raise AttributeError('Invalid setting: \'{}\''.format(attr))

        attr_value = self.settings.get(attr)
        setattr(self, attr, attr_value)

        return attr_value


settings = Settings()
