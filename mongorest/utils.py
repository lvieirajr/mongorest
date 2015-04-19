# -*- encoding: UTF-8 -*-

from bson.objectid import ObjectId

__all__ = [
    'serialize',
    'deserialize',
]


def serialize(to_serialize):
    """
    Recursively serializes the passed value (to_serialize)
    Converting all the values to JSON-Accepted values.
    """
    if isinstance(to_serialize, (str, int, float)):
        return to_serialize

    elif isinstance(to_serialize, ObjectId):
        return str(to_serialize)

    elif isinstance(to_serialize, dict):
        return to_serialize.__class__({
            serialize(key): serialize(value)
            for (key, value) in to_serialize.items()
        })

    elif isinstance(to_serialize, (list, tuple)):
        return to_serialize.__class__(
            serialize(value) for value in to_serialize
        )

    elif hasattr(to_serialize, '__iter__'):
        return list(serialize(value) for value in to_serialize)

    return to_serialize


def deserialize(to_deserialize):
    """
    Recursively deserializes the passed value (to_deserialize)
    Converting all the possible values back to its original forms
    """
    if isinstance(to_deserialize, str):
        if to_deserialize == str(ObjectId(to_deserialize)):
            return ObjectId(to_deserialize)
        else:
            return to_deserialize

    elif isinstance(to_deserialize, dict):
        return to_deserialize.__class__({
            deserialize(key): deserialize(value)
            for (key, value) in to_deserialize.items()
        })

    elif isinstance(to_deserialize, (list, tuple)):
        return to_deserialize.__class__(
            deserialize(value) for value in to_deserialize
        )

    elif hasattr(to_deserialize, '__iter__'):
        return list(deserialize(value) for value in to_deserialize)

    return to_deserialize
