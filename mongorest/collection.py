# -*- encoding: UTF-8 -*-

import six

from .database import db
from .document import Document
from .settings import settings
from .utils import serialize

__all__ = [
    'Collection',
]


class CollectionMeta(type):
    """
    MetaClass for the Collection Class.
    Prepares the member dict adding the correct collection based on the name,
    And the meta dict, with empty required and optional (fields)
    """

    @classmethod
    def __prepare__(mcs, name, bases):
        """
        Returns the collection based on the name of the Class
        Also the meta dict to serve as a base
        """
        return {
            'collection': db[name.lower()],
            'meta': {
                'required': {},
                'optional': {},
            },
        }


class Collection(six.with_metaclass(CollectionMeta, object)):
    """
    Base class for Collections.
    Can Serialize and De-Serialize the data.
    """

    def __new__(cls, *args, **kwargs):
        """
        Instantiating a Collection will return a Document from that Collection
        """
        return Document(cls, *args, **kwargs)

    @classmethod
    def find_one(cls, filter=None, serialized=settings.SERIALIZE):
        """
        Returns one document dict if at least one passes the filter
        Otherwise returns None
        Will return the serialized dict if serialized=True
        """
        document = cls.collection.find_one(filter)
        return serialize(document) if serialized else document

    @classmethod
    def find(cls, filter=None, serialized=settings.SERIALIZE):
        """
        Returns all document dicts that pass the filter
        Will return the serialized dict if serialized=True
        """
        documents = list(cls.collection.find(filter))
        return serialize(documents) if serialized else documents

    @classmethod
    def aggregate(cls, pipeline, serialized=settings.SERIALIZE):
        """
        Returns the list of document dicts returned from the Aggregate Pipeline
        Will return the serialized document dicts if serialized=True
        """
        documents = list(cls.collection.aggregate(pipeline))
        return serialize(documents) if serialized else documents

    @classmethod
    def insert_one(cls, document, serialized=settings.SERIALIZE):
        """
        Inserts a document into the Collection
        Returns the inserted document's _id
        Will return the serialized _id if serialized=True
        """
        _id = cls.collection.insert_one(document).inserted_id
        return serialize(_id) if serialized else _id

    @classmethod
    def insert_many(cls, documents, ordered=True, serialized=settings.SERIALIZE):
        """
        Inserts a list of documents into the Collection
        Returns the all the inserted documents' _ids
        Will return the serialized _ids if serialized=True
        """
        _ids = list(cls.collection.insert_many(documents, ordered).inserted_ids)
        return serialize(_ids) if serialized else _ids

    @classmethod
    def update_one(cls, filter, update, upsert=False, serialized=settings.SERIALIZE):
        """
        Updates a document that passes the filter
        Returns the raw result of the update
        Will return the serialized raw result if serialized=True
        """
        updated = cls.collection.update_one(filter, update, upsert).raw_result
        return serialize(updated) if serialized else updated

    @classmethod
    def update_many(cls, filter, update, upsert=False, serialized=settings.SERIALIZE):
        """
        Updates all the documents that pass the filter
        Returns the raw result of the update
        Will return the serialized raw result if serialized=True
        """
        updated = cls.collection.update_many(filter, update, upsert).raw_result
        return serialize(updated) if serialized else updated

    @classmethod
    def replace_one(cls, filter, replacement, upsert=False, serialized=settings.SERIALIZE):
        """
        Replaces a document that passes the filter
        Returns the raw result of the replace
        Will return the serialized raw result if serialized=True
        """
        replaced = cls.collection.replace_one(filter, replacement, upsert).raw_result
        return serialize(replaced) if serialized else replaced

    @classmethod
    def delete_one(cls, filter, serialized=settings.SERIALIZE):
        """
        Deletes a document that passes the filter
        Returns the raw result of the delete
        Will return the serialized raw result if serialized=True
        """
        deleted = cls.collection.delete_one(filter).raw_result
        return serialize(deleted) if serialized else deleted

    @classmethod
    def delete_many(cls, filter, serialized=settings.SERIALIZE):
        """
        Deletes all the documents that pass the filter
        Returns the raw result of the delete
        Will return the serialized raw result if serialized=True
        """
        deleted = cls.collection.delete_many(filter).raw_result
        return serialize(deleted) if serialized else deleted

    @classmethod
    def count(cls, filter=None):
        """
        Returns the number of documents that pass the filter
        """
        return len(cls.find(filter, serialized=False))

    @classmethod
    def get(cls, filter=None):
        """
        Returns a Document Object if any document passes the filter
        Returns None otherwise
        """
        document = Document(
            cls=cls,
            fields=cls.find_one(filter, serialized=False),
            processed=True
        )
        return document if document.fields(serialized=False) else None
