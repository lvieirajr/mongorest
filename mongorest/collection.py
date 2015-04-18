# -*- encoding: UTF-8 -*-

from bson.objectid import ObjectId

from mongorest.database import db

__all__ = [
    'Collection',
]


class CollectionMeta(type):
    """
    MetaClass for the Collection Class.
    Prepares the member dict adding the correct collection based on the name,
    And adds the required_fields dict.
    """
    @classmethod
    def __prepare__(mcs, name, bases):
        """
        Returns the collection based on the name of the Class
        Also an empty required_fields dict to serve as a base
        """
        return {
            'collection': db[name.lower()],
            'required_fields': {},
        }


class Collection(object, metaclass=CollectionMeta):
    """
    Base class for Collections.
    Can Serialize and De-Serialize the data.
    """
    def __init__(self, fields=None):
        self._fields = fields or {}
        self._errors = {}

    def __getattr__(self, attr):
        if attr in ('_fields', '_errors'):
            return object.__getattribute__(self, attr)
        elif attr in self._fields:
            return self._fields[attr]
        else:
            return object.__getattribute__(self, attr)

    def __setattr__(self, attr, value):
        if attr in ('_fields', '_errors'):
            object.__setattr__(self, attr, value)
        else:
            self._fields[attr] = value

    @classmethod
    def serialized(cls, to_serialize):
        if isinstance(to_serialize, (str, int, float)):
            return to_serialize

        elif isinstance(to_serialize, ObjectId):
            return str(to_serialize)

        elif isinstance(to_serialize, dict):
            return to_serialize.__class__({
                cls.serialized(key): cls.serialized(value)
                for (key, value) in to_serialize.items()
            })

        elif isinstance(to_serialize, (list, tuple)):
            return to_serialize.__class__(
                cls.serialized(value) for value in to_serialize
            )

        elif hasattr(to_serialize, '__iter__'):
            return list(cls.serialized(value) for value in to_serialize)

        return to_serialize

    @classmethod
    def deserialized(cls, to_deserialize):
        if isinstance(to_deserialize, str):
            if to_deserialize == str(ObjectId(to_deserialize)):
                return ObjectId(to_deserialize)
            else:
                return to_deserialize

        elif isinstance(to_deserialize, dict):
            return to_deserialize.__class__({
                cls.deserialized(key): cls.deserialized(value)
                for (key, value) in to_deserialize.items()
            })

        elif isinstance(to_deserialize, (list, tuple)):
            return to_deserialize.__class__(
                cls.deserialized(value) for value in to_deserialize
            )

        elif hasattr(to_deserialize, '__iter__'):
            return list(cls.deserialized(value) for value in to_deserialize)

        return to_deserialize

    @classmethod
    def find_one(cls, filter=None, serialize=False):
        document = cls.collection.find_one(filter)
        return cls.serialized(document) if serialize else document

    @classmethod
    def find(cls, filter=None, serialize=False):
        documents = list(cls.collection.find(filter))
        return cls.serialized(documents) if serialize else documents

    @classmethod
    def aggregate(cls, pipeline, serialize=False):
        documents = list(cls.collection.aggregate(pipeline))
        return cls.serialized(documents) if serialize else documents

    @classmethod
    def get(cls, filter=None, serialize=False):
        document = cls(fields=cls.find_one(filter, serialize))
        return document if document.pk else None

    @classmethod
    def insert_one(cls, document, serialize=False):
        _id = cls.collection.insert_one(document).inserted_id
        return cls.serialized(_id) if serialize else _id

    @classmethod
    def insert_many(cls, documents, ordered=True, serialize=False):
        _ids = cls.collection.insert_many(documents, ordered).inserted_ids
        return cls.serialized(_ids) if serialize else _ids

    @classmethod
    def update_one(cls, filter, update, upsert=False, serialize=False):
        updated = cls.collection.udpate_one(filter, update, upsert).raw_result
        return cls.serialized(updated) if serialize else updated

    @classmethod
    def update_many(cls, filter, update, upsert=False, serialize=False):
        updated = cls.collection.udpate_many(filter, update, upsert).raw_result
        return cls.serialized(updated) if serialize else updated

    @classmethod
    def delete_one(cls, filter, serialize=False):
        deleted = cls.collection.delete_one(filter).raw_result
        return cls.serialized(deleted) if serialize else deleted

    @classmethod
    def delete_many(cls, filter, serialize=False):
        deleted = cls.collection.delete_many(filter).raw_result
        return cls.serialized(deleted) if serialize else deleted

    @classmethod
    def count(cls, filter=None):
        return cls.find(filter).count()

    @property
    def pk(self):
        return self._fields.get('_id')
