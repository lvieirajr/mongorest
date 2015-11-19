# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals


from bson.objectid import ObjectId
from collections import Mapping
try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict
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
        collection = document.collection
        collection_name = collection.__name__

        validated, errors = self.validate(document.fields), {}
        for key, _error in self.flattened_errors.items():
            field = key
            field_schema = self.get_field_schema(field)

            error = None
            if _error == 'unknown field':
                error = UnknownFieldError(collection_name, field)
            elif _error == 'required field':
                error = RequiredFieldError(collection_name, field)
            elif _error == 'field is read-only':
                error = ReadOnlyFieldError(collection_name, field)
            elif _error.startswith('must be of') and _error.endswith('type'):
                error = FieldTypeError(
                    collection_name, field, field_schema['type']
                )

            if error and isinstance(error, SchemaValidationError):
                if 'error_code' in errors:
                    errors['errors'].append(error)
                else:
                    errors = DocumentValidationError(
                        collection_name, self.schema, document.fields, [error]
                    )

        document._errors = errors
        return not bool(document.errors)

    @property
    def flattened_errors(self):
        return self.flatten(self._errors, '', '.')

    def flatten(self, mapping, parent='', separator='.'):
        items = []

        mapping = OrderedDict(
            sorted(
                [key_value for key_value in mapping.items()],
                key=lambda key_value: key_value[0]
            )
        )
        for key, value in mapping.items():
            flat_key = separator.join([parent, str(key)]).strip(separator)

            if isinstance(value, Mapping):
                items.extend(self.flatten(value, flat_key, separator).items())
            else:
                items.append((flat_key, value))

        return OrderedDict(items)

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
