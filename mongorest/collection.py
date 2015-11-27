# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import inspect
from re import sub
from six import with_metaclass
from types import MethodType

from .database import db
from .decorators import serializable
from .document import Document
from .validator import Validator

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
            collection = sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            collection = sub('([a-z0-9])([A-Z])', r'\1_\2', collection.lower())

            members['collection'] = db[collection]

        if 'schema' not in members:
            members['schema'] = {}

        if 'allow_unknown' not in members:
            members['allow_unknown'] = True

        members['validator'] = Validator(
            schema=members['schema'],
            allow_unknown=members['allow_unknown']
        )

        return super(mcs, mcs).__new__(mcs, *(name, bases, members), **kwargs)

    def __getattr__(self, attr):
        """
        Tries to find the attribute in the underlying PyMongo collection
        If it can't find it defaults to returning the attribute from self
        """
        if hasattr(self.collection, attr):
            attribute = getattr(self.collection, attr)

            if inspect.isfunction(attribute):
                attribute = MethodType(attribute, self)

            return attribute
        else:
            raise AttributeError


class Collection(with_metaclass(CollectionMeta, object)):
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
        Updates a document that passes the filter with the update value
        Will upsert a new document if upsert=True and no document is filtered
        """
        return cls.collection.update_one(filter, update, upsert).raw_result

    @classmethod
    @serializable
    def update_many(cls, filter, update, upsert=False):
        """
        Updates all documents that pass the filter with the update value
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
    def get(cls, filter=None, preprocess=False, postprocess=False, **kwargs):
        """
        Returns a Document if any document is filtered, returns None otherwise
        """
        document = Document(
            cls, cls.collection.find_one(filter, **kwargs), preprocess,
            postprocess
        )
        return document if document.fields else None

    @classmethod
    def documents(cls, filter=None, preprocess=False, postprocess=False,
                  **kwargs):
        """
        Returns a list of Documents if any document is filtered
        """
        return [
            Document(cls, document, preprocess, postprocess)
            for document in cls.collection.find(filter, **kwargs)
        ]

    def restrict_unique(self):
        """
        Should return False if uniqueness restriction is not enforced or if
        document passes the restrictions enforced.
        Should return an error dict if uniqueness restriction is enforced and
        document does not pass the restrictions enforced.
        Should be overwritten by subclasses.
        """
        return False

    def restrict_update(self):
        """
        Should return False if update restriction is not enforced or if
        document passes the restrictions enforced.
        Should return an error dict if update restriction is enforced and
        document does not pass the restrictions enforced.
        Should be overwritten by subclasses.
        """
        return False

    def cascade_update(self):
        """
        Should cascade the update to the required documents after the given
        document was updated.
        Should be overwritten by subclasses.
        """
        pass

    def restrict_delete(self):
        """
        Should return False if delete restriction is not enforced or if
        document passes the restrictions enforced.
        Should return an error dict if delete restriction is enforced and
        document does not pass the restrictions enforced.
        Should be overwritten by subclasses.
        """
        return False

    def cascade_delete(self):
        """
        Should cascade the delete to the required documents after the given
        document was deleted.
        Should be overwritten by subclasses.
        """
        pass
