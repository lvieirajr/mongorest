# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from bson.json_util import dumps, loads

__all__ = [
    'deserialize',
    'serialize',
]


def deserialize(to_deserialize):
    """
    Deserializes a string into a PyMongo BSON
    """
    return loads(to_deserialize)


def serialize(to_serialize):
    """
    Serializes a PyMongo BSON into a string
    """
    return dumps(to_serialize)
