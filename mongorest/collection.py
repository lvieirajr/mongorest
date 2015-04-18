# -*- encoding: UTF-8 -*-

from .database import db
from .utils import serialize

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
    """

    def __init__(self, data=None):
        self._data = data
        self._fields = {}
        self._errors = {}

    def __getattr__(self, attr):
        try:
            return self._fields[attr]
        except KeyError:
            return object.__getattribute__(self, attr)

    def __setattr__(self, attr, value):
        if attr == '_fields':
            object.__setattr__(self, attr, value)
        else:
            self._fields[attr] = value

    @classmethod
    def find_one(cls, filter=None, serialized=False):
        document = cls.collection.find_one(filter)

        if serialized:
            for (key, value) in document.items():
                document[key] = serialize(value)

        return document

    @classmethod
    def find(cls, filter=None, serialized=False):
        documents = list(cls.collection.find(filter))

        if documents and serialized:
            for document in documents:
                for (key, value) in document.items():
                    document[key] = serialize(value)

        return documents

    @classmethod
    def aggregate(cls, pipeline, serialized=False):
        documents = list(cls.collection.aggregate(pipeline))

        if documents and serialized:
            for document in documents:
                for (key, value) in document.items():
                    document[key] = serialize(value)

        return documents

    @classmethod
    def count(cls, filter=None):
        return cls.find(filter).count()

    @classmethod
    def get(cls, filter=None, serialized=False):
        document = None
        fields = cls.find_one(filter, serialized)

        if fields:
            document = cls()
            document._fields = fields

        return document

    def pk(self, serialized=False):
        if serialized:
            return serialize(self._fields['_id'])

        return self._fields['_id']
