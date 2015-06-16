# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from pymongo.errors import PyMongoError
from types import MethodType, FunctionType

__all__ = [
    'Document',
]


class Document(object):
    """
    Document Class
    It will know how to validate its fields
    Will use the meta of the Collection to do so.
    """

    def __init__(self, collection, fields=None, processed=False):
        """
        Initializes the Document Object with the given attributes
        Processes the fields if not processed
        Then validates the fields based on the Collection
        """
        super(Document, self).__init__()

        self._collection = collection
        self._fields = fields or {}
        self._errors = {}

        if not processed:
            self._process()

        self._validate()

    def __getattr__(self, attr):
        """
        Tries to get the attribute on the following order:
        First checks if the attribute is one of:
        (__new__, _collection, _fields, _errors, get)
        Second checks if the attribute is in _fields
        Third checks if the attribute is in _collection
        If none of them is found, tries to get the attribute from self
        """
        if attr in ('__new__', '_collection', '_fields', '_errors', 'get'):
            return object.__getattribute__(self, attr)

        elif attr in self._fields:
            return self._fields[attr]

        elif hasattr(self._collection, attr):
            attribute = getattr(self._collection, attr)

            if type(attribute) == FunctionType:
                return MethodType(attribute, self)

            return attribute

        else:
            return object.__getattribute__(self, attr)

    def __setattr__(self, attr, value):
        """
        Tries to set the value to attr in the following order:
        Checks if the attribute is one of (_collection, _fields, _errors)
        If it is not, it will set the value in _fields[attr]
        """
        if attr in ('_collection', '_fields', '_errors'):
            object.__setattr__(self, attr, value)
        else:
            self._fields[attr] = value

    def __repr__(self):
        """
        Returns the representation of the Object formated like:
        <{Collection Name}Document object at {hex location of the object}>
        """
        return '<Document<{0}> object at {1}>'.format(
            self._collection.__name__, hex(id(self)),
        )

    def _validate(self):
        """
        Validates if the required fields are present on the Document
        Validates if the required fields are of the correct types
        If one of these two validations fail, add an error to self._errors
        """
        fields = dict(
            self.meta.get('optional', {}), **self.meta.get('required', {})
        )

        for (field, type_or_tuple) in list(fields.items()):
            if field in self._fields:
                if not isinstance(self._fields[field], type_or_tuple):
                    if isinstance(type_or_tuple, (tuple, list)):
                        types = ' or '.join(t.__name__ for t in type_or_tuple)
                    else:
                        types = type_or_tuple.__name__

                    self._errors[field] = \
                        'Field \'{0}\' must be of type(s): {1}.'.format(
                            field, types
                        )
            elif field in self.meta.get('required', {}):
                self._errors[field] = 'Field \'{0}\' is required.'.format(
                    field
                )

    def _process(self):
        """
        Calls every collection method that starts with 'process'.
        Does this in order to process the values on the fields
        So they will be ready to be saved on the Database
        """
        for attr in dir(self._collection):
            if attr.lower().startswith('process'):
                self.__getattr__(attr)()

    @property
    def is_valid(self):
        """
        Returns True if no errors have been found, False otherwise.
        """
        return len(self._errors) == 0

    @property
    def fields(self):
        """
        Returns the document's fields
        """
        return self._fields

    @property
    def errors(self):
        """
        Returns the document's errors
        """
        return self._errors

    def save(self):
        """
        Saves the Document to the database if it is valid.
        Returns the error dict otherwise.
        If the Document does not contain an _id it will insert a new Document
        If the Document contains an _id it will be replaced instead of inserted
        """
        if self.is_valid:
            try:
                if '_id' in self._fields:
                    self.replace_one(
                        {'_id': self._id}, self._fields, upsert=True
                    )
                else:
                    self._fields['_id'] = self.insert_one(self._fields)
            except PyMongoError as error:
                self._errors['save'] = error.details.get(
                    'errmsg', error.details.get('err', 'Error.')
                )
                return self._errors

            return self._id
        else:
            return self._errors
