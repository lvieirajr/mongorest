# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from bson.objectid import ObjectId
from collections import Mapping
from cerberus import Validator as CerberusValidator

from .errors import *

__all__ = [
    'Validator',
]


class Validator(CerberusValidator):

    def __init__(self, schema=None, allow_unknown=True, **kwargs):
        super(Validator, self).__init__(
            schema=schema or {}, allow_unknown=allow_unknown, **kwargs
        )

    def _validate_type_objectid(self, field, value):
        if not isinstance(value, ObjectId):
            self._error(field, 'must be of ObjectId type')

    def validate_document(self, document):
        self.schema = document.schema
        collection_name, errors = type(document).__name__, {}

        self.validate(document.document)
        for key, _errors in self.flattened_errors.items():
            field = key
            field_schema = self.get_field_schema(field)

            _errors = [_errors] if not isinstance(_errors, list) else _errors
            for _error in _errors:
                error = None

                if _error == 'unknown field':
                    error = UnknownFieldError(collection_name, field)
                elif _error == 'required field':
                    error = RequiredFieldError(collection_name, field)
                elif _error == 'field is read-only':
                    error = ReadOnlyFieldError(collection_name, field)
                elif _error.startswith('must be ') and _error.endswith('type'):
                    type_or_types = field_schema['type']

                    if isinstance(type_or_types, list):
                        type_or_types = ' or '.join(type_or_types)

                    error = FieldTypeError(
                        collection_name, field, type_or_types
                    )
                elif 'does not match regex' in _error:
                    error = RegexMatchError(
                        collection_name, field,
                        _error.split('match regex \'')[1][:-1]
                    )
                elif _error.startswith('min length is'):
                    error = MinLengthError(
                        collection_name, field, field_schema['minlength']
                    )
                elif _error.startswith('max length is'):
                    error = MaxLengthError(
                        collection_name, field, field_schema['maxlength']
                    )
                elif _error.startswith('length of '):
                    error = LengthError(
                        collection_name, field, len(field_schema['items'])
                    )
                elif _error.startswith('unallowed value '):
                    error = ValueNotAllowedError(
                        collection_name, field,
                        _error.split('unallowed value ')[1]
                    )
                elif _error.startswith('unallowed values '):
                    error = ValuesNotAllowedError(
                        collection_name, field,
                        _error.split('unallowed values ')[1]
                    )
                elif _error.startswith('min value is '):
                    error = MinValueError(
                        collection_name, field, field_schema['min']
                    )
                elif _error.startswith('max value is '):
                    error = MaxValueError(
                        collection_name, field, field_schema['max']
                    )

                if error and isinstance(error, SchemaValidationError):
                    try:
                        errors['errors'].append(error)
                    except KeyError:
                        errors = DocumentValidationError(
                            collection_name, self.schema, document.document,
                            [error]
                        )

        if errors:
            if 'errors' in errors:
                errors['errors'] = sorted(
                    errors['errors'], key=lambda e: e['field']
                )

            document._errors = errors
            return False

        return True

    @property
    def flattened_errors(self):
        return self.flatten(self._errors, '', '.')

    def flatten(self, mapping, parent='', separator='.'):
        items = []

        for key, value in mapping.items():
            flat_key = separator.join([parent, str(key)]).strip(separator)

            if isinstance(value, Mapping):
                items.extend(self.flatten(value, flat_key, separator).items())
            else:
                items.append((flat_key, value))

        return dict(items)

    def get_field_schema(self, field):
        schema, fields = self.schema, field.split('.')

        for field in fields:
            if field in schema:
                schema = schema.get(field)
            elif 'schema' in schema and field in schema.get('schema'):
                schema = schema.get('schema').get(field)
            elif 'schema' in schema:
                schema = schema.get('schema')

        return schema
