# -*- encoding: UTF-8 -*-

from bson.objectid import ObjectId

__all__ = [
    'serialize',
]


def serialize(value):
    if isinstance(value, ObjectId):
        return str(value)
    else:
        return value