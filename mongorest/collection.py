# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import six

from .database import db
from .decorators import ensure_indexes, serializable

__all__ = [
    'Collection',
]


class CollectionMeta(type):
    """
    MetaClass for the Collection Class.
    Prepares the member dict adding the correct collection based on the name,
    And the meta dict, with empty required and optional (fields)
    """

    def __new__(mcs, *args, **kwargs):
        name = args[0]
        bases = args[1]
        members = args[2].copy()

        if 'collection' not in members:
            members['collection'] = db[name.lower()]

        if 'meta' not in members:
            members['meta'] = {
                'required': {},
                'optional': {},
            }

        return super(mcs, mcs).__new__(mcs, *(name, bases, members), **kwargs)


class Collection(six.with_metaclass(CollectionMeta, object)):
    """
    Base Class for Collections.
    """

    @ensure_indexes
    def __new__(cls, *args, **kwargs):
        """
        Instantiating a Collection will return a Document from that Collection
        """
        from .document import Document
        return Document(cls, *args, **kwargs)

    @classmethod
    def indexes(cls):
        """
        Creates indexes required by the collection
        """
        cls.collection.create_index('_id')

    @classmethod
    @serializable
    @ensure_indexes
    def find_one(cls, filter=None, *args, **kwargs):
        """
        Returns one document dict if at least one passes the filter
        Returns None otherwise.
        """
        return cls.collection.find_one(filter, *args, **kwargs)

    @classmethod
    @serializable
    @ensure_indexes
    def find(cls, *args, **kwargs):
        """
        Returns all document dicts that pass the filter
        """
        return list(cls.collection.find(*args, **kwargs))

    @classmethod
    @serializable
    @ensure_indexes
    def aggregate(cls, pipeline=None, **kwargs):
        """
        Returns the document dicts returned from the Aggregation Pipeline
        """
        return list(cls.collection.aggregate(pipeline or [], **kwargs))

    @classmethod
    @ensure_indexes
    def insert_one(cls, document):
        """
        Inserts a document into the Collection and returns its _id
        """
        return cls.collection.insert_one(document).inserted_id

    @classmethod
    @ensure_indexes
    def insert_many(cls, documents, ordered=True):
        """
        Inserts a list of documents into the Collection and returns their _ids
        """
        return cls.collection.insert_many(documents, ordered).inserted_ids

    @classmethod
    @ensure_indexes
    def update_one(cls, filter, update, upsert=False):
        """
        Updates a document that passes the filter with the udpate value
        Will upsert a new document if upsert=True and no document is filtered
        """
        return cls.collection.update_one(filter, update, upsert).raw_result

    @classmethod
    @ensure_indexes
    def update_many(cls, filter, update, upsert=False):
        """
        Updates all documents that pass the filter with the udpate value
        Will upsert a new document if upsert=True and no document is filtered
        """
        return cls.collection.update_many(filter, update, upsert).raw_result

    @classmethod
    @ensure_indexes
    def replace_one(cls, filter, replacement, upsert=False):
        """
        Replaces a document that passes the filter.
        Will upsert a new document if upsert=True and no document is filtered
        """
        return cls.collection.replace_one(
            filter, replacement, upsert
        ).raw_result

    @classmethod
    @ensure_indexes
    def delete_one(cls, filter):
        """
        Deletes one document that passes the filter
        """
        return cls.collection.delete_one(filter).raw_result

    @classmethod
    @ensure_indexes
    def delete_many(cls, filter):
        """
        Deletes all documents that pass the filter
        """
        return cls.collection.delete_many(filter).raw_result

    @classmethod
    @ensure_indexes
    def count(cls, filter=None, with_limit_and_skip=False):
        """
        Returns the number of documents that pass the filter
        """
        return cls.collection.find(filter).count(with_limit_and_skip)

    @classmethod
    @ensure_indexes
    def get(cls, filter=None, **kwargs):
        """
        Returns a Document if any document is filtered, returns None otherwise
        """
        from .document import Document
        document = Document(
            cls, cls.collection.find_one(filter, **kwargs), True
        )
        return document if document.fields else None
