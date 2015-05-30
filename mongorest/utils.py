# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from bson.json_util import dumps, loads
from os.path import abspath

__all__ = [
    'deserialize',
    'load_module',
    'serialize',
]


def deserialize(to_deserialize):
    """
    Deserializes a string into a PyMongo BSON
    """
    return loads(to_deserialize)


def load_module(module):
    try:
        from importlib import import_module
        return import_module(module)
    except ImportError:
        from imp import load_source
        return load_source(
            'module',
            abspath('{0}.py'.format(module.replace('.', '/')))
        )


def serialize(to_serialize):
    """
    Serializes a PyMongo BSON into a string
    """
    return dumps(to_serialize)
