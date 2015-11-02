# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__all__ = [
    'MongoRestError',
    'PyMongoError',
    'ValidationError',
    'RequiredFieldError',
    'FieldTypeError',
    'UnidentifiedDocumentError',
    'DocumentNotFoundError',
    'DocumentNotUpdatedError',
]


class MongoRestError(dict):

    def __init__(self, error_code=None, error_type=None):
        super(MongoRestError, self).__init__({
            'error_code': error_code,
            'error_type': error_type,
        })


class PyMongoError(MongoRestError):

    def __init__(self, message=None, operation=None, collection=None,
                 document=None):
        super(PyMongoError, self).__init__(0, 'PyMongoError')

        self['error_message'] = message
        self['collection'] = collection
        self['document'] = document
        self['operation'] = operation


class ValidationError(MongoRestError):

    def __init__(self, errors=None, collection=None, document=None):
        super(ValidationError, self).__init__(1, 'ValidationError')

        self['error_message'] = '{0} document validation failed.'.format(
            collection
        )
        self['errors'] = errors or []
        self['collection'] = collection
        self['document'] = document


class RequiredFieldError(MongoRestError):

    def __init__(self, field=None):
        super(RequiredFieldError, self).__init__(2, 'RequiredFieldError')

        self['error_message'] = 'Field \'{0}\' is required.'.format(field)
        self['field'] = field


class FieldTypeError(MongoRestError):

    def __init__(self, field=None, types=None):
        super(FieldTypeError, self).__init__(3, 'FieldTypeError')

        self['error_message'] = 'Field \'{0}\' must be of type(s): {1}.' \
                                ''.format(field, types)
        self['field'] = field
        self['types'] = types


class UnidentifiedDocumentError(MongoRestError):

    def __init__(self, collection=None, document=None):
        super(UnidentifiedDocumentError, self).__init__(
            4, 'UnidentifiedDocumentError'
        )

        self['error_message'] = 'The given {0} document has no _id.'.format(
            collection
        )
        self['collection'] = collection
        self['document'] = document


class DocumentNotFoundError(MongoRestError):

    def __init__(self, collection=None, _id=None):
        super(DocumentNotFoundError, self).__init__(5, 'DocumentNotFoundError')

        self['error_message'] = '{0} is not a valid {1} document _id.'.format(
            _id, collection
        )
        self['collection'] = collection
        self['_id'] = _id


class DocumentNotUpdatedError(MongoRestError):

    def __init__(self, collection=None, _id=None, document=None):
        super(DocumentNotUpdatedError, self).__init__(
            6, 'DocumentNotUpdatedError'
        )

        self['error_message'] = 'No fields were updated for {0} document ' \
                                'with _id {1}.'.format(collection, _id)
        self['collection'] = collection
        self['_id'] = _id
        self['document'] = document
