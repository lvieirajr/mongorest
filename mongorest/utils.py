# -*- encoding: UTF-8 -*-

from bson.json_util import dumps as mongo_dumps, loads as mongo_loads
from json import loads as json_loads, dumps as json_dumps

__all__ = [
    'serialize',
    'deserialize',
]


def serialize(to_serialize):
    """
    Recursively serializes the passed value (to_serialize)
    Converting all the values to JSON-Accepted values.
    """
    return json_loads(mongo_dumps(to_serialize))


def deserialize(to_deserialize):
    """
    Recursively deserializes the passed value (to_deserialize)
    Converting all the possible values back to its original forms
    """
    return mongo_loads(json_dumps(to_deserialize))
