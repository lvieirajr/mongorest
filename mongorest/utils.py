# -*- encoding: UTF-8 -*-

from bson.json_util import dumps as mongo_dumps, loads as mongo_loads
from datetime import datetime
from json import loads as json_loads, dumps as json_dumps

__all__ = [
    'serialize',
    'deserialize',
]


def serialize(to_serialize):
    """
    Serializes a Mongo BSON into a JSON
    """
    return json_loads(mongo_dumps(to_serialize))


def deserialize(to_deserialize):
    """
    Deserializes a JSON into a PyMongo BSON
    """
    return mongo_loads(json_dumps(to_deserialize))


def end_of_day(date):
    """
    Returns the given date at the time 23:59:59
    """
    return datetime.combine(date.date(), datetime.max.time())


def beginning_of_day(date):
    """
    Returns the given date at the time 00:00:00
    """
    return datetime.combine(date.date(), datetime.min.time())
