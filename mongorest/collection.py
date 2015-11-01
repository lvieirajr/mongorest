# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import six
from types import MethodType, FunctionType

from .decorators import serializable
from .document import Document

__all__ = [
    'Collection',
]


class CollectionMeta(type):
    """
    MetaClass that knows how to get its own DB Collection
    """

    def __new__(mcs, *args, **kwargs):
        name = args[0]
        bases = args[1]
        members = args[2].copy()

        if 'collection' not in members:
            from .database import db
            members['collection'] = db[name.lower()]

        if 'meta' not in members:
            members['meta'] = {
                'required': {},
                'optional': {},
            }

        return super(mcs, mcs).__new__(mcs, *(name, bases, members), **kwargs)

    def __getattr__(self, attr):
        """
        Tries to find the attribute in the underlying PyMongo collection
        If it can't find it defaults to returning the attribute from self
        """
        if hasattr(self.collection, attr):
            attribute = getattr(self.collection, attr)

            if type(attribute) == FunctionType:
                return MethodType(attribute, self)

            return attribute
        else:
            return object.__getattribute__(self, attr)


class Collection(six.with_metaclass(CollectionMeta, object)):
    """
    Base Class for Collections.
    """

    def __new__(cls, *args, **kwargs):
        """
        Instantiating a Collection will return a Document from that Collection
        """
        return Document(cls, *args, **kwargs)

    @classmethod
    @serializable
    def find_one(cls, filter=None, *args, **kwargs):
        """
        Returns one document dict if at least one passes the filter
        Returns None otherwise.
        """
        return cls.collection.find_one(filter, *args, **kwargs)

    @classmethod
    @serializable
    def find(cls, *args, **kwargs):
        """
        Returns all document dicts that pass the filter
        """
        return list(cls.collection.find(*args, **kwargs))

    @classmethod
    @serializable
    def aggregate(cls, pipeline=None, **kwargs):
        """
        Returns the document dicts returned from the Aggregation Pipeline
        """
        return list(cls.collection.aggregate(pipeline or [], **kwargs))

    @classmethod
    @serializable
    def insert_one(cls, document):
        """
        Inserts a document into the Collection and returns its _id
        """
        return cls.collection.insert_one(document).inserted_id

    @classmethod
    @serializable
    def insert_many(cls, documents, ordered=True):
        """
        Inserts a list of documents into the Collection and returns their _ids
        """
        return cls.collection.insert_many(documents, ordered).inserted_ids

    @classmethod
    @serializable
    def update_one(cls, filter, update, upsert=False):
        """
        Updates a document that passes the filter with the udpate value
        Will upsert a new document if upsert=True and no document is filtered
        """
        return cls.collection.update_one(filter, update, upsert).raw_result

    @classmethod
    @serializable
    def update_many(cls, filter, update, upsert=False):
        """
        Updates all documents that pass the filter with the udpate value
        Will upsert a new document if upsert=True and no document is filtered
        """
        return cls.collection.update_many(filter, update, upsert).raw_result

    @classmethod
    @serializable
    def replace_one(cls, filter, replacement, upsert=False):
        """
        Replaces a document that passes the filter.
        Will upsert a new document if upsert=True and no document is filtered
        """
        return cls.collection.replace_one(
            filter, replacement, upsert
        ).raw_result

    @classmethod
    @serializable
    def delete_one(cls, filter):
        """
        Deletes one document that passes the filter
        """
        return cls.collection.delete_one(filter).raw_result

    @classmethod
    @serializable
    def delete_many(cls, filter):
        """
        Deletes all documents that pass the filter
        """
        return cls.collection.delete_many(filter).raw_result

    @classmethod
    @serializable
    def count(cls, filter=None, **kwargs):
        """
        Returns the number of documents that pass the filter
        """
        return cls.collection.count(filter, **kwargs)

    @classmethod
    def get(cls, filter=None, **kwargs):
        """
        Returns a Document if any document is filtered, returns None otherwise
        """
        document = Document(
            cls, cls.collection.find_one(filter, **kwargs), True
        )
        return document if document.fields else None

    @classmethod
    def documents(cls, filter=None, **kwargs):
        """
        Returns a list of Documents if any document is filtered
        """
        return [
            Document(cls, document, True)
            for document in cls.collection.find(filter, **kwargs)
        ]

    @classmethod
    def is_unique(cls, document):
        return True
