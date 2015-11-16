# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from collections import Mapping
from cerberus import Validator

__all__ = [
    'MongoRestValidator',
]


class MongoRestValidator(Validator):

    def validate_document(self, document):
        self.validate(document.fields)

        for key, error in self.flattened_errors:
            pass

        return bool(document.errors)

    @property
    def flattened_errors(self):
        return self.flatten(self._errors, '', '.')

    def flatten(self, mapping, parent='', separator='.'):
        items = []

        for key, value in mapping.items():
            flat_key = separator.join([parent, key]).strip(separator)

            if isinstance(value, Mapping):
                items.extend(self.flatten(value, flat_key, separator).items())
            else:
                items.append((flat_key, value))

        return dict(items)
