# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__all__ = [
    'MongoRestError',
    'PyMongoError',
    'SchemaMissingError',
    'SchemaTypeError',
    'SchemaFieldTypeError',
    'UnknownRuleError',
    'FieldDefinitionError',
    'UnknownTypeError',
    'DocumentMissingError',
    'DocumentTypeError',
    'UnidentifiedDocumentError',
    'DocumentNotFoundError',
    'SchemaValidationError',
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
]


# Base Error: -1
class MongoRestError(dict):

    def __init__(self, error_code=-1, error_type='MongoRestError'):
        super(MongoRestError, self).__init__([
            ('error_code', error_code), ('error_type', error_type),
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


# Schema Errors: 10 - 19
class SchemaMissingError(MongoRestError):

    def __init__(self, collection=None):
        super(SchemaMissingError, self).__init__(10, 'SchemaMissingError')

        self['error_message'] = 'Validation schema for collection \'{0}\' ' \
                                'is missing.'.format(collection)
        self['collection'] = collection


class SchemaTypeError(MongoRestError):

    def __init__(self, collection=None, schema=None):
        super(SchemaTypeError, self).__init__(11, 'SchemaTypeError')

        self['error_message'] = 'Validation schema for collection \'{0}\' ' \
                                'must be a dict.'.format(collection)
        self['collection'] = collection
        self['schema'] = schema


class SchemaFieldTypeError(MongoRestError):

    def __init__(self, collection=None, field=None):
        super(SchemaFieldTypeError, self).__init__(12, 'SchemaFieldTypeError')

        self['error_message'] = 'Type of field \'{0}\' on collection ' \
                                '\'{1}\' must be either a list or a ' \
                                'dict.'.format(field, collection)
        self['collection'] = collection
        self['field'] = field


class UnknownRuleError(MongoRestError):

    def __init__(self, collection=None, field=None, rule=None):
        super(UnknownRuleError, self).__init__(13, 'UnknownRuleError')

        self['error_message'] = 'Unknown rule \'{0}\' for field \'{1}\' ' \
                                'on collection \'{2}\'.'.format(
                                    rule, field, collection
                                )
        self['collection'] = collection
        self['field'] = field
        self['rule'] = rule


class FieldDefinitionError(MongoRestError):

    def __init__(self, collection=None, field=None, rule=None):
        super(FieldDefinitionError, self).__init__(14, 'FieldDefinitionError')

        self['error_message'] = 'Schema definition for field \'{0}\' on ' \
                                'collection \'{1}\' must be a dict.'.format(
                                    field, collection
                                )
        self['collection'] = collection
        self['field'] = field


class UnknownTypeError(MongoRestError):

    def __init__(self, collection=None, field=None, field_type=None):
        super(UnknownTypeError, self).__init__(15, 'UnknownTypeError')

        self['error_message'] = 'Type \'{0}\' for field \'{1}\' was not ' \
                                'recognized on the validation schema for ' \
                                'collection \'{2}\'.'.format(
                                    field_type, field, collection
                                )
        self['collection'] = collection
        self['field'] = field
        self['type'] = field_type


# Document Errors: 20 - 29
class DocumentMissingError(MongoRestError):

    def __init__(self, collection=None):
        super(DocumentMissingError, self).__init__(20, 'DocumentMissingError')

        self['error_message'] = 'Document missing for collection \'{0}\'.' \
                                ''.format(collection)
        self['collection'] = collection


class DocumentTypeError(MongoRestError):

    def __init__(self, collection=None, document=None):
        super(DocumentTypeError, self).__init__(21, 'DocumentTypeError')

        self['error_message'] = 'Document for collection \'{0}\' must ' \
                                'be a dict.'.format(collection)
        self['collection'] = collection
        self['document'] = document


class UnidentifiedDocumentError(MongoRestError):

    def __init__(self, collection=None, document=None):
        super(UnidentifiedDocumentError, self).__init__(
            22, 'UnidentifiedDocumentError'
        )

        self['error_message'] = 'The given document from collection \'{0}\' ' \
                                'has no _id.'.format(collection)
        self['collection'] = collection
        self['document'] = document


class DocumentNotFoundError(MongoRestError):

    def __init__(self, collection=None, _id=None):
        super(DocumentNotFoundError, self).__init__(
            23, 'DocumentNotFoundError'
        )

        self['error_message'] = '{0} is not a valid _id for a document from ' \
                                'collection \'{1}\'.'.format(_id, collection)
        self['collection'] = collection
        self['_id'] = _id


# Validation Error: 30
class SchemaValidationError(MongoRestError):

    def __init__(self, collection=None, schema=None, document=None,
                 errors=None):
        super(SchemaValidationError, self).__init__(
            30, 'SchemaValidationError'
        )

        self['error_message'] = 'Validation of document from collection ' \
                                '\'{0}\' failed.'.format(collection)
        self['collection'] = collection
        self['schema'] = schema
        self['document'] = document
        self['errors'] = errors or []


# Field Validation Errors: 31 - 99
class UnknownFieldError(MongoRestError):

    def __init__(self, collection=None, field=None):
        super(UnknownFieldError, self).__init__(31, 'UnknownFieldError')

        self['error_message'] = 'Field \'{0}\' on collection \'{1}\' is ' \
                                'unknown.'.format(field, collection)
        self['collection'] = collection
        self['field'] = field


class RequiredFieldError(MongoRestError):

    def __init__(self, collection=None, field=None):
        super(RequiredFieldError, self).__init__(32, 'RequiredFieldError')

        self['error_message'] = 'Field \'{0}\' on collection \'{1}\' is ' \
                                'required.'.format(field, collection)
        self['collection'] = collection
        self['field'] = field


class ReadOnlyFieldError(MongoRestError):

    def __init__(self, collection=None, field=None, length=None):
        super(ReadOnlyFieldError, self).__init__(33, 'ReadOnlyFieldError')

        self['error_message'] = 'Field \'{0}\' on collection \'{1}\' is ' \
                                'read only.'.format(field, collection)
        self['collection'] = collection
        self['field'] = field


class FieldTypeError(MongoRestError):

    def __init__(self, collection=None, field=None, field_type=None):
        super(FieldTypeError, self).__init__(34, 'FieldTypeError')

        self['error_message'] = 'Field \'{0}\' on collection \'{1}\' must ' \
                                'be of type \'{2}\'.'.format(
                                    field, collection, field_type
                                )
        self['collection'] = collection
        self['field'] = field
        self['type'] = field_type


class RegexMatchError(MongoRestError):

    def __init__(self, collection=None, field=None, regex=None):
        super(RegexMatchError, self).__init__(35, 'RegexMatchError')

        self['error_message'] = 'Value does not match the regex \'{0}\' for ' \
                                'field \'{1}\' on collection \'{2}\'.'.format(
                                    regex, field, collection
                                )
        self['collection'] = collection
        self['field'] = field
        self['regex'] = regex


class MinLengthError(MongoRestError):

    def __init__(self, collection=None, field=None, min_length=None):
        super(MinLengthError, self).__init__(36, 'MinLengthError')

        self['error_message'] = 'Minimum length for field \'{0}\' on ' \
                                'collection \'{1}\' is {2}.'.format(
                                    field, collection, min_length
                                )
        self['collection'] = collection
        self['field'] = field
        self['min_length'] = min_length


class MaxLengthError(MongoRestError):

    def __init__(self, collection=None, field=None, max_length=None):
        super(MaxLengthError, self).__init__(37, 'MaxLengthError')

        self['error_message'] = 'Maximum length for field \'{0}\' on ' \
                                'collection \'{1}\' is {2}.'.format(
                                    field, collection, max_length
                                )
        self['collection'] = collection
        self['field'] = field
        self['max_length'] = max_length


class LengthError(MongoRestError):

    def __init__(self, collection=None, field=None, length=None):
        super(LengthError, self).__init__(38, 'LengthError')

        self['error_message'] = 'Length of field \'{0}\' on collection ' \
                                '\'{1}\' must be {2}.'.format(
                                    field, collection, length
                                )
        self['collection'] = collection
        self['field'] = field
        self['length'] = length


class ValueNotAllowedError(MongoRestError):

    def __init__(self, collection=None, field=None, value=None):
        super(ValueNotAllowedError, self).__init__(39, 'ValueNotAllowedError')

        self['error_message'] = 'Value \'{0}\' is not allowed for field ' \
                                '\'{1}\' on collection \'{2}\'.'.format(
                                    value, field, collection
                                )
        self['collection'] = collection
        self['field'] = field
        self['value'] = value


class ValuesNotAllowedError(MongoRestError):

    def __init__(self, collection=None, field=None, values=None):
        super(ValuesNotAllowedError, self).__init__(
            40, 'ValuesNotAllowedError'
        )

        self['error_message'] = 'Values \'{0}\' are not allowed for field ' \
                                '\'{1}\' on collection \'{2}\'.'.format(
                                    values, field, collection
                                )
        self['collection'] = collection
        self['field'] = field
        self['values'] = values


class MinValueError(MongoRestError):

    def __init__(self, collection=None, field=None, min_value=None):
        super(MinValueError, self).__init__(41, 'MinValueError')

        self['error_message'] = 'Minimum value for field \'{0}\' on ' \
                                'collection \'{1}\' is {2}.'.format(
                                    field, collection, min_value
                                )
        self['collection'] = collection
        self['field'] = field
        self['min_value'] = min_value


class MaxValueError(MongoRestError):

    def __init__(self, collection=None, field=None, max_value=None):
        super(MaxValueError, self).__init__(42, 'MaxValueError')

        self['error_message'] = 'Maximum value for field \'{0}\' on ' \
                                'collection \'{1}\' is {2}.'.format(
                                    field, collection, max_value
                                )
        self['collection'] = collection
        self['field'] = field
        self['max_value'] = max_value


class EmptyNotAllowedError(MongoRestError):

    def __init__(self, collection=None, field=None):
        super(EmptyNotAllowedError, self).__init__(43, 'EmptyNotAllowedError')

        self['error_message'] = 'Empty values are not allowed for field ' \
                                '\'{0}\' on collection \'{1}\'.'.format(
                                    field, collection
                                )
        self['collection'] = collection
        self['field'] = field


class NullNotAllowedError(MongoRestError):

    def __init__(self, collection=None, field=None):
        super(NullNotAllowedError, self).__init__(44, 'NullNotAllowedError')

        self['error_message'] = 'Null values are not allowed for field ' \
                                '\'{0}\' on collection \'{1}\'.'.format(
                                    field, collection
                                )
        self['collection'] = collection
        self['field'] = field


class DependencyError(MongoRestError):

    def __init__(self, collection=None, field=None, dependency=None):
        super(DependencyError, self).__init__(45, 'DependencyError')

        self['error_message'] = 'Field \'{0}\' on collection \'{1}\' is ' \
                                'required if field \'{2}\' is present.'.format(
                                    field, collection, dependency
                                )
        self['collection'] = collection
        self['field'] = field
        self['dependency'] = dependency


class ValueDependencyError(MongoRestError):

    def __init__(self, collection=None, field=None, dependency=None,
                 dependency_values=None):
        super(ValueDependencyError, self).__init__(46, 'ValueDependencyError')

        self['error_message'] = 'Field \'{0}\' on collection \'{1}\' is ' \
                                'required to have values \'{2}\' if field ' \
                                '\'{3}\' is present.'.format(
                                    field, collection, dependency_values,
                                    dependency
                                )
        self['collection'] = collection
        self['field'] = field
        self['dependency'] = dependency
        self['dependency_values'] = dependency_values


class CoercionError(MongoRestError):

    def __init__(self, collection=None, field=None, coercion_type=None):
        super(CoercionError, self).__init__(47, 'CoercionError')

        self['error_message'] = 'Field \'{0}\' on collection \'{1}\' ' \
                                'could not be coerced into type \'{2}\'.' \
                                ''.format(field, collection, coercion_type)
        self['collection'] = collection
        self['field'] = field
        self['coercion_type'] = coercion_type
