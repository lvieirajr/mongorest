# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__all__ = [
    'MongoRestError',
    'PyMongoError',
    'DocumentError',
    'UnidentifiedDocumentError',
    'DocumentNotFoundError',
    'SchemaValidationError',
    'DocumentValidationError',
    'UnknownFieldError',
    'RequiredFieldError',
    'ReadOnlyFieldError',
    'FieldTypeError',
    'RegexMatchError',
    'MinLengthError',
    'MaxLengthError',
    'LengthError',
    'ValueNotAllowedError',
    'ValuesNotAllowedError',
    'MinValueError',
    'MaxValueError',
    'EmptyNotAllowedError',
    'NullNotAllowedError',
    'DependencyError',
    'ValueDependencyError',
    'CoercionError',
]


# MongoRestError: -1
class MongoRestError(dict):

    def __init__(self, error_code=-1, error_type='MongoRestError',
                 error_message='MongoRestError'):
        super(MongoRestError, self).__init__([
            ('error_code', error_code),
            ('error_type', error_type),
            ('error_message', error_message)
        ])


# PyMongo Errors: 0 - 9
class PyMongoError(MongoRestError):

    def __init__(self, error_message=None, operation=None, collection=None,
                 document=None):
        super(PyMongoError, self).__init__(0, 'PyMongoError')

        self['error_message'] = error_message
        self['operation'] = operation
        self['collection'] = collection
        self['document'] = document


# Document Errors: 10 - 19
class DocumentError(MongoRestError):

    def __init__(self, error_code=10, error_type='DocumentError',
                 error_message='DocumentError'):
        super(DocumentError, self).__init__(
            error_code, error_type, error_message
        )


class UnidentifiedDocumentError(DocumentError):

    def __init__(self, collection=None, document=None):
        super(UnidentifiedDocumentError, self).__init__(
            11,
            'UnidentifiedDocumentError',
            'The given document from collection \'{0}\' has no _id.'.format(
                collection
            )
        )

        self['collection'] = collection
        self['document'] = document


class DocumentNotFoundError(DocumentError):

    def __init__(self, collection=None, _id=None):
        super(DocumentNotFoundError, self).__init__(
            12,
            'DocumentNotFoundError',
            '{0} is not a valid _id for a document from collection \'{1}\'.'
            ''.format(_id, collection)
        )

        self['collection'] = collection
        self['_id'] = _id


# Schema Validation Errors: 20 - 99
class SchemaValidationError(MongoRestError):

    def __init__(self, error_code=20, error_type='SchemaValidationError',
                 error_message='SchemaValidationError'):
        super(SchemaValidationError, self).__init__(
            error_code, error_type, error_message
        )


class DocumentValidationError(SchemaValidationError):

    def __init__(self, collection=None, schema=None, document=None,
                 errors=None):
        super(DocumentValidationError, self).__init__(
            21,
            'DocumentValidationError',
            'Validation of document from collection \'{0}\' failed.'.format(
                collection
            )
        )

        self['collection'] = collection
        self['schema'] = schema
        self['document'] = document
        self['errors'] = errors or []


class UnknownFieldError(SchemaValidationError):

    def __init__(self, collection=None, field=None):
        super(UnknownFieldError, self).__init__(
            22,
            'UnknownFieldError',
            'Field \'{0}\' on collection \'{1}\' is unknown.'.format(
                field, collection
            )
        )

        self['collection'] = collection
        self['field'] = field


class RequiredFieldError(SchemaValidationError):

    def __init__(self, collection=None, field=None):
        super(RequiredFieldError, self).__init__(
            23,
            'RequiredFieldError',
            'Field \'{0}\' on collection \'{1}\' is required.'.format(
                field, collection
            )
        )

        self['collection'] = collection
        self['field'] = field


class ReadOnlyFieldError(SchemaValidationError):

    def __init__(self, collection=None, field=None):
        super(ReadOnlyFieldError, self).__init__(
            24,
            'ReadOnlyFieldError',
            'Field \'{0}\' on collection \'{1}\' is read only.'.format(
                field, collection
            )
        )

        self['collection'] = collection
        self['field'] = field


class FieldTypeError(SchemaValidationError):

    def __init__(self, collection=None, field=None, field_type=None):
        super(FieldTypeError, self).__init__(
            25,
            'FieldTypeError',
            'Field \'{0}\' on collection \'{1}\' must be of type {2}.'
            ''.format(field, collection, field_type)
        )

        self['collection'] = collection
        self['field'] = field
        self['type'] = field_type


class RegexMatchError(SchemaValidationError):

    def __init__(self, collection=None, field=None, regex=None):
        super(RegexMatchError, self).__init__(
            26,
            'RegexMatchError',
            'Value does not match the regex \'{0}\' for field \'{1}\' on '
            'collection \'{2}\'.'.format(regex, field, collection)
        )

        self['collection'] = collection
        self['field'] = field
        self['regex'] = regex


class MinLengthError(SchemaValidationError):

    def __init__(self, collection=None, field=None, min_length=None):
        super(MinLengthError, self).__init__(
            27,
            'MinLengthError',
            'Minimum length for field \'{0}\' on collection \'{1}\' is '
            '{2}.'.format(field, collection, min_length)
        )

        self['collection'] = collection
        self['field'] = field
        self['min_length'] = min_length


class MaxLengthError(SchemaValidationError):

    def __init__(self, collection=None, field=None, max_length=None):
        super(MaxLengthError, self).__init__(
            28,
            'MaxLengthError',
            'Maximum length for field \'{0}\' on collection \'{1}\' is '
            '{2}.'.format(field, collection, max_length)
        )

        self['collection'] = collection
        self['field'] = field
        self['max_length'] = max_length


class LengthError(SchemaValidationError):

    def __init__(self, collection=None, field=None, length=None):
        super(LengthError, self).__init__(
            29,
            'LengthError',
            'Length of field \'{0}\' on collection \'{1}\' must be {2}.'
            ''.format(field, collection, length)
        )

        self['collection'] = collection
        self['field'] = field
        self['length'] = length


class ValueNotAllowedError(SchemaValidationError):

    def __init__(self, collection=None, field=None, value=None):
        super(ValueNotAllowedError, self).__init__(
            30,
            'ValueNotAllowedError',
            'Value \'{0}\' is not allowed for field \'{1}\' on collection '
            '\'{2}\'.'.format(value, field, collection),
        )

        self['collection'] = collection
        self['field'] = field
        self['value'] = value


class ValuesNotAllowedError(SchemaValidationError):

    def __init__(self, collection=None, field=None, values=None):
        super(ValuesNotAllowedError, self).__init__(
            31,
            'ValuesNotAllowedError',
            'Values \'{0}\' are not allowed for field \'{1}\' on collection '
            '\'{2}\'.'.format(values, field, collection)
        )

        self['collection'] = collection
        self['field'] = field
        self['values'] = values


class MinValueError(SchemaValidationError):

    def __init__(self, collection=None, field=None, min_value=None):
        super(MinValueError, self).__init__(
            32,
            'MinValueError',
            'Minimum value for field \'{0}\' on collection \'{1}\' is '
            '{2}.'.format(field, collection, min_value)
        )

        self['collection'] = collection
        self['field'] = field
        self['min_value'] = min_value


class MaxValueError(SchemaValidationError):

    def __init__(self, collection=None, field=None, max_value=None):
        super(MaxValueError, self).__init__(
            33,
            'MaxValueError',
            'Maximum value for field \'{0}\' on collection \'{1}\' is '
            '{2}.'.format(field, collection, max_value)
        )

        self['collection'] = collection
        self['field'] = field
        self['max_value'] = max_value


class EmptyNotAllowedError(SchemaValidationError):

    def __init__(self, collection=None, field=None):
        super(EmptyNotAllowedError, self).__init__(
            34,
            'EmptyNotAllowedError',
            'Empty values are not allowed for field \'{0}\' on collection '
            '\'{1}\'.'.format(field, collection)
        )

        self['collection'] = collection
        self['field'] = field


class NullNotAllowedError(SchemaValidationError):

    def __init__(self, collection=None, field=None):
        super(NullNotAllowedError, self).__init__(
            35,
            'NullNotAllowedError',
            'Null values are not allowed for field \'{0}\' on collection '
            '\'{1}\'.'.format(field, collection)
        )

        self['collection'] = collection
        self['field'] = field


class DependencyError(SchemaValidationError):

    def __init__(self, collection=None, field=None, dependency=None):
        super(DependencyError, self).__init__(
            36,
            'DependencyError',
            'Field \'{0}\' on collection \'{1}\' is required if field '
            '\'{2}\' is present.'.format(field, collection, dependency)
        )

        self['collection'] = collection
        self['field'] = field
        self['dependency'] = dependency


class ValueDependencyError(SchemaValidationError):

    def __init__(self, collection=None, field=None, dependency=None,
                 dependency_values=None):
        super(ValueDependencyError, self).__init__(
            37,
            'ValueDependencyError',
            'Field \'{0}\' on collection \'{1}\' is required to have values '
            '\'{2}\' if field \'{3}\' is present.'.format(
                field, collection, dependency_values, dependency
            )
        )

        self['collection'] = collection
        self['field'] = field
        self['dependency'] = dependency
        self['dependency_values'] = dependency_values


class CoercionError(SchemaValidationError):

    def __init__(self, collection=None, field=None, coercion_type=None):
        try:
            coercion_type_repr = repr(coercion_type).split('\'')[1]
        except IndexError:
            coercion_type_repr = repr(coercion_type).strip('\'')

        super(CoercionError, self).__init__(
            38,
            'CoercionError',
            'Field \'{0}\' on collection \'{1}\' could not be coerced into '
            '{2}.'.format(
                field, collection, coercion_type_repr
            )
        )

        self['collection'] = collection
        self['field'] = field
        self['coercion_type'] = coercion_type
