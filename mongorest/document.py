# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from pymongo.errors import PyMongoError
from types import MethodType, FunctionType

from .decorators import serializable

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
        First checks if the attribute is in _fields
        Second checks if the attribute is in _collection
        If none of them is found, tries to get the attribute from self
        """
        if attr in self._fields:
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
        <Document<{%Collection Name%}> object at {%object id%}>
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

        validation_error = {
            'error_code': 1,
            'error_type': 'ValidationError',
            'error_message': 'Document validation failed.',
            'errors': [],
            'document': self._fields,
            'collection': self.collection.__name__,
        }

        for (field, type_or_tuple) in list(fields.items()):
            if field in self._fields:
                if not isinstance(self._fields[field], type_or_tuple):
                    if isinstance(type_or_tuple, (tuple, list)):
                        types = ' or '.join(t.__name__ for t in type_or_tuple)
                    else:
                        types = type_or_tuple.__name__

                    if 'error_code' not in self._errors:
                        self._errors = validation_error

                    self._errors['errors'].append({
                        'error_code': 3,
                        'error_type': 'FieldTypeError',
                        'error_message': 'Field \'{0}\' must be of type(s): '
                                         '{1}.'.format(field, types),
                        'field': field,
                    })
            elif field in self.meta.get('required', {}):
                if 'error_code' not in self._errors:
                    self._errors = validation_error

                self._errors['errors'].append({
                    'error_code': 2,
                    'error_type': 'RequiredFieldError',
                    'error_message': 'Field \'{0}\' is required.'.format(
                        field
                    ),
                    'field': field,
                })

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
    def collection(self):
        """
        Returns the Collection of the Document
        """
        return self._collection

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

    @property
    def is_valid(self):
        """
        Returns True if no errors have been found, False otherwise.
        """
        return not len(self._errors)

    @serializable
    def save(self):
        """
        Saves the Document to the database if it is valid.
        Returns the error dict otherwise.
        If the Document does not contain an _id it will insert a new Document
        If the Document contains an _id it will be replaced instead of inserted
        """
        if self.is_valid:
            restricted = self.restrict_unique(self)
            if restricted:
                return restricted

            try:
                self._fields['_id'] = self.insert_one(self._fields)
                return self._fields
            except PyMongoError as exc:
                return {
                    'error_code': 0,
                    'error_type': 'PyMongoError',
                    'error_message':  exc.details.get(
                        'errmsg', exc.details.get(
                            'err', 'PyMongoError.'
                        )
                    ),
                    'document': self._fields,
                    'collection': self.collection.__name__,
                    'operation': 'save',
                }

        return self._errors

    @serializable
    def update(self):
        """
        Updates the document with it's current fields if it is already
        saved in the collection
        """
        if self.is_valid:
            if '_id' in self._fields:
                restricted = self.restrict_unique(self)
                if restricted:
                    return restricted

                restricted = self.restrict_update(self)
                if restricted:
                    return restricted

                try:
                    replaced = self.replace_one(
                        {'_id': self._id}, self._fields
                    )

                    if replaced['nModified'] == 1:
                        self.cascade_update(self)
                        return self._fields
                    elif replaced['nMatched'] == 0:
                        return {
                            'error_code': 5,
                            'error_type': 'DocumentNotFoundError',
                            'error_message': '{0} is not a valid {1} document '
                                             '_id.'.format(
                                                    repr(self._id),
                                                    self.collection.__name__
                                                ),
                            '_id': self._id,
                            'collection': self.collection.__name__,
                        }
                    else:
                        return {
                            'error_code': 6,
                            'error_type': 'DocumentNotUpdatedError',
                            'error_message': 'No fields were updated for {0} '
                                             'document with _id {1}.'
                                             'updated.'.format(
                                                    self.collection.__name__,
                                                    repr(self._id),
                                                ),
                            'document': self._fields,
                            '_id': self._id,
                            'collection': self.collection.__name__,
                        }
                except PyMongoError as exc:
                    return {
                        'error_code': 0,
                        'error_type': 'PyMongoError',
                        'error_message':  exc.details.get(
                            'errmsg', exc.details.get(
                                'err', 'PyMongoError.'
                            )
                        ),
                        'document': self._fields,
                        'collection': self.collection.__name__,
                        'operation': 'update',
                    }
            else:
                return {
                    'error_code': 4,
                    'error_type': 'UnidentifiedDocumentError',
                    'error_message': 'The given {0} document has no _id.'
                                     ''.format(self.collection.__name__),
                    'document': self._fields,
                    'collection': self.collection.__name__,
                }

        return self._errors

    @serializable
    def delete(self):
        """
        Deletes the document if it is already saved in the collection
        """
        if '_id' in self._fields:
            restricted = self.restrict_delete(self)
            if restricted:
                return restricted

            try:
                deleted = self.delete_one({'_id': self._id})

                if deleted['n'] == 1:
                    self.cascade_delete(self)
                    return self._fields
                else:
                    return {
                        'error_code': 5,
                        'error_type': 'DocumentNotFoundError',
                        'error_message': '{0} is not a valid {1} document _id.'
                                         ''.format(
                                                repr(self._id),
                                                self.collection.__name__
                                            ),
                        '_id': self._id,
                        'collection': self.collection.__name__,
                    }
            except PyMongoError as exc:
                return {
                    'error_code': 0,
                    'error_type': 'PyMongoError',
                    'error_message':  exc.details.get(
                        'errmsg', exc.details.get(
                            'err', 'PyMongoError.'
                        )
                    ),
                    'document': self._fields,
                    'collection': self.collection.__name__,
                    'operation': 'delete',
                }
        else:
            return {
                'error_code': 4,
                'error_type': 'UnidentifiedDocumentError',
                'error_message': 'The given {0} document has no _id.'.format(
                    self.collection.__name__,
                ),
                'document': self._fields,
                'collection': self.collection.__name__,
            }
