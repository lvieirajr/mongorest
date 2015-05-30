# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import six

from .decorators import ensure_indexes, serializable
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


class Collection(six.with_metaclass(CollectionMeta, object)):
    """
    Base Class for Collections.
    """

    @ensure_indexes
    def __new__(cls, *args, **kwargs):
        """
        Instantiating a Collection will return a Document from that Collection
        """
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
    def find_one(cls, query=None, *args, **kwargs):
        """
        Returns one document dict if at least one passes the filter
        Returns None otherwise.
        """
        return cls.collection.find_one(query, *args, **kwargs)

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
    def update_one(cls, query, update, upsert=False):
        """
        Updates a document that passes the filter with the udpate value
        Will upsert a new document if upsert=True and no document is filtered
        """
        return cls.collection.update_one(query, update, upsert).raw_result

    @classmethod
    @ensure_indexes
    def update_many(cls, query, update, upsert=False):
        """
        Updates all documents that pass the filter with the udpate value
        Will upsert a new document if upsert=True and no document is filtered
        """
        return cls.collection.update_many(query, update, upsert).raw_result

    @classmethod
    @ensure_indexes
    def replace_one(cls, query, replacement, upsert=False):
        """
        Replaces a document that passes the filter.
        Will upsert a new document if upsert=True and no document is filtered
        """
        return cls.collection.replace_one(
            query, replacement, upsert
        ).raw_result

    @classmethod
    @ensure_indexes
    def delete_one(cls, query):
        """
        Deletes one document that passes the filter
        """
        return cls.collection.delete_one(query).raw_result

    @classmethod
    @ensure_indexes
    def delete_many(cls, query):
        """
        Deletes all documents that pass the filter
        """
        return cls.collection.delete_many(query).raw_result

    @classmethod
    @ensure_indexes
    def count(cls, query=None, with_limit_and_skip=False):
        """
        Returns the number of documents that pass the filter
        """
        return cls.collection.find(query).count(with_limit_and_skip)

    @classmethod
    @ensure_indexes
    def get(cls, query=None, **kwargs):
        """
        Returns a Document if any document is filtered, returns None otherwise
        """
        document = Document(
            cls, cls.collection.find_one(query, **kwargs), True
        )
        return document if document.fields else None
