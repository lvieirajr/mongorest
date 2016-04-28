# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import re

from bson.json_util import dumps as bson_dumps, loads as bson_loads
from bson.objectid import ObjectId
from six import string_types

__all__ = [
    'deserialize',
    'serialize',
]


def deserialize(to_deserialize, *args, **kwargs):
    """
    Deserializes a string into a PyMongo BSON
    """
    if isinstance(to_deserialize, string_types):
        if re.match('^[0-9a-f]{24}$', to_deserialize):
            return ObjectId(to_deserialize)
        try:
            return bson_loads(to_deserialize, *args, **kwargs)
        except:
            return bson_loads(bson_dumps(to_deserialize), *args, **kwargs)
    else:
        return bson_loads(bson_dumps(to_deserialize), *args, **kwargs)


def serialize(to_serialize, *args, **kwargs):
    """
    Serializes a PyMongo BSON into a string
    """
    return bson_dumps(to_serialize, *args, **kwargs)
