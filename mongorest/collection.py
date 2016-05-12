# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import copy
import inspect
import re
import six
import types

from pymongo.errors import PyMongoError as PyMongoException

from .decorators import serializable
from .errors import (
    PyMongoError,
    DocumentNotFoundError,
    UnidentifiedDocumentError
)
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

        from .database import db
        if 'collection' not in members:
            members['collection'] = db[
                re.sub(
                    '((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))', '_\1', name
                ).lower()
            ]

        if 'schema' not in members:
            members['schema'] = {}

        if 'allow_unknown' not in members:
            members['allow_unknown'] = True

        members['validator'] = Validator(
            schema=members['schema'],
            allow_unknown=members['allow_unknown']
        )

        return super(mcs, mcs).__new__(mcs, *(name, bases, members), **kwargs)

    def __getattr__(self, name):
        """
        Returns the attribute from the _document if it exists.
        Returns it from the collection if not on _document, but on collection.
        """
        if name in dir(self.collection):
            attribute = getattr(self.collection, name)

            if inspect.isfunction(attribute):
                attribute = types.MethodType(attribute, self)

            return attribute
        else:
            raise AttributeError(name)


class Collection(six.with_metaclass(CollectionMeta, object)):
    """
    Base Class for Collections.
    """

    def __init__(self, document=None):
        self._document = copy.deepcopy(document or {})
        self._errors = {}

        if not self.before_validation():
            if self.validator.validate_document(self):
                self._document = self.validator.document

                if not self.after_validation():
                    self.after_validation_succeeded()
            else:
                if not self.after_validation():
                    self.after_validation_failed()

    def __repr__(self):
        """
        Returns the representation of the Object formated like:
        <Document<{%Collection Name%}> object at {%object id%}>
        """
        return '<Document<{0}> object at {1}>'.format(
            type(self).__name__, hex(id(self)),
        )

    def __setattr__(self, key, value):
        """
        Sets the value to the given key if it is one of the specified keys.
        Sets the given key on the _document to the given value otherwise.
        """
        keys = {
            'collection', 'schema', 'allow_unknown', '_document', '_errors'
        }

        if key in keys:
            object.__setattr__(self, key, value)
        else:
            self._document[key] = value

    def __getattr__(self, name):
        """
        Returns the attribute from the _document if it exists.
        Returns it from the collection if not on _document, but on collection.
        """
        if name in self._document:
            return self._document[name]
        elif name in dir(self.collection):
            attribute = getattr(self.collection, name)

            if inspect.isfunction(attribute):
                attribute = types.MethodType(attribute, self)

            return attribute
        else:
            raise AttributeError(name)

    def __deepcopy__(self, memo):
        copy = self.__class__(self._document)
        memo[id(self)] = copy

        return copy

    @property
    def document(self):
        """
        Returns the document
        """
        return self._document

    @property
    def errors(self):
        """
        Returns the validation errors
        """
        return self._errors

    @property
    def is_valid(self):
        """
        Returns True if no validation errors have been found, False otherwise.
        """
        return not self._errors

    @serializable
    def insert(self, **kwargs):
        """
        Saves the Document to the database if it is valid.
        Returns errors otherwise.
        """
        if self.is_valid:
            before = self.before_insert()
            if before:
                return before

            try:
                self._document['_id'] = self.insert_one(self._document)

                self.after_insert()

                return self._document
            except PyMongoException as exc:
                return PyMongoError(
                    error_message=exc.details.get(
                        'errmsg', exc.details.get('err', 'PyMongoError.')
                    ),
                    operation='insert', collection=type(self).__name__,
                    document=self._document,
                )

        return self._errors

    @serializable
    def update(self, **kwargs):
        """
        Updates the document with the given _id saved in the collection
        """
        if self.is_valid:
            if '_id' in self._document:
                to_update = self.find_one({'_id': self._id})

                if to_update:
                    before = self.before_update(old=to_update)
                    if before:
                        return before

                    try:
                        self.replace_one({'_id': self._id}, self._document)

                        self.after_update(old=to_update)

                        return self._document
                    except PyMongoException as exc:
                        return PyMongoError(
                            error_message=exc.details.get(
                                'errmsg', exc.details.get(
                                    'err', 'PyMongoError.'
                                )
                            ),
                            operation='update', collection=type(self).__name__,
                            document=self._document,
                        )
                else:
                    return DocumentNotFoundError(type(self).__name__, self._id)
            else:
                return UnidentifiedDocumentError(
                    type(self).__name__, self._document
                )

        return self._errors

    @serializable
    def delete(self, **kwargs):
        """
        Deletes the document if it is saved in the collection
        """
        if self.is_valid:
            if '_id' in self._document:
                to_update = self.find_one({'_id': self._id})

                if to_update:
                    before = self.before_delete()
                    if before:
                        return before

                    try:
                        self.delete_one({'_id': self._id})

                        self.after_delete()

                        return self._document
                    except PyMongoException as exc:
                        return PyMongoError(
                            error_message=exc.details.get(
                                'errmsg', exc.details.get(
                                    'err', 'PyMongoError.'
                                )
                            ),
                            operation='delete', collection=type(self).__name__,
                            document=self._document,
                        )
                else:
                    return DocumentNotFoundError(type(self).__name__, self._id)
            else:
                return UnidentifiedDocumentError(
                    type(self).__name__, self._document
                )

    @classmethod
    @serializable
    def find_one(cls, filter=None, *args, **kwargs):
        """
        Returns one document dict if one passes the filter.
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
    def get(cls, filter=None, **kwargs):
        """
        Returns a Document if any document is filtered, returns None otherwise
        """
        document = cls(cls.find_one(filter, **kwargs))
        return document if document.document else None

    @classmethod
    def documents(cls, filter=None, **kwargs):
        """
        Returns a list of Documents if any document is filtered
        """
        documents = [cls(document) for document in cls.find(filter, **kwargs)]
        return [document for document in documents if document.document]

    def before_validation(self):
        return

    def after_validation(self):
        return

    def after_validation_failed(self):
        return

    def after_validation_succeeded(self):
        return

    def before_insert(self):
        return

    def after_insert(self):
        return

    def before_update(self, old):
        return

    def after_update(self, old):
        return

    def before_delete(self):
        return

    def after_delete(self):
        return
