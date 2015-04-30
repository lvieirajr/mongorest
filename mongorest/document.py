# -*- encoding: UTF-8 -*-

from types import MethodType, FunctionType

from .settings import settings
from .utils import serialize

__all__ = [
    'Document',
]


class Document(object):
    """
    Document Class
    It will know how to validate its fields
    Will use the meta of the Collection to do so.
    """

    def __init__(self, cls, fields=None, processed=False):
        """
        Initializes the Document Object with the given attributes
        Then validates the fields based on the Collection
        """
        super(Document, self).__init__()

        self._cls = cls
        self._fields = fields or {}
        self._errors = {}

        self._validate()

        if not processed:
            self._process()

    def __getattr__(self, attr):
        """
        Tries to get the attribute on the following order:
        First checks if the attribute is one of:
        (__new__, _cls, _fields, _errors, get)
        Second checks if the attribute is in _fields
        Third checks if the attribute is in _cls
        If none of them is found, tries to get the attribute from self
        """
        if attr in ('__new__', '_cls', '_fields', '_errors', 'get'):
            return object.__getattribute__(self, attr)

        elif attr in self._fields:
            return self._fields[attr]

        elif hasattr(self._cls, attr):
            attribute = getattr(self._cls, attr)

            if type(attribute) == FunctionType:
                return MethodType(attribute, self)

            return attribute

        else:
            return object.__getattribute__(self, attr)

    def __setattr__(self, attr, value):
        """
        Tries to set the value to attr in the following order:
        Checks if the attribute is one of (_cls, _fields, _errors)
        If it is not, it will set the value in _fields[attr]
        """
        if attr in ('_cls', '_fields', '_errors'):
            object.__setattr__(self, attr, value)
        else:
            self._fields[attr] = value

    def __repr__(self):
        """
        Returns the representation of the Object formated like:
        <{Collection Name}Document object at {hex location of the object}>
        """
        return '<{}Document object at {}>'.format(
            self._cls.__name__,
            hex(id(self)),
        )

    def _validate(self):
        """
        Validates if the required fields are present on the Document
        Validates if the required fields are of the correct types
        If one of these two validations fail, add an error to self._errors
        """
        fields = dict(
            self.meta.get('optional', {}),
            **self.meta.get('required', {})
        )

        for (field, type_or_tuple) in fields.items():
            if field in self._fields:
                if not isinstance(self._fields[field], type_or_tuple):
                    if isinstance(type_or_tuple, (tuple, list)):
                        types = ' or '.join(t.__name__ for t in type_or_tuple)
                    else:
                        types = type_or_tuple.__name__

                    self._errors[field] = \
                        'Field \'{}\' must be of type(s): {}.'.format(
                            field, types
                        )
            elif field in self.meta.get('required', {}):
                self._errors[field] = 'Field \'{}\' is required.'.format(field)

    def _process(self):
        """
        Calls every collection method that starts with process.
        Does this in order to process the values on the fields
        So they will be ready to be saved on the Database
        """
        for attr in dir(self._cls):
            if attr.lower().startswith('process'):
                self.__getattr__(attr)()

    @property
    def is_valid(self):
        """
        Returns True if no errors have been found, False otherwise.
        """
        return len(self._errors) == 0

    def fields(self, serialized=settings.SERIALIZE):
        """
        Returns the document's fields
        Will return the serialized fields if serialized=True
        """
        return serialize(self._fields) if serialized else self._fields

    def errors(self, serialized=settings.SERIALIZE):
        """
        Returns the document's errors
        Will return the serialized errors if serialized=True
        """
        return serialize(self._errors) if serialized else self._errors

    def get(self, field, serialized=settings.SERIALIZE):
        """
        Returns the field if it exists in _fields, returns None otherwise
        Will return the serialized field if serialized=True
        """
        field = self._fields.get(field)
        return serialize(field) if serialized else field

    def save(self, serialized=settings.SERIALIZE):
        """
        Saves the Document to the database if it is valid.
        Returns the error dict otherwise.
        If the Document does not contain an _id it will insert a new Document
        If the Document contains an _id it will be updated instead of inserted
        """
        if self.is_valid:
            if self.get('_id', serialized=False):
                self.replace_one({'_id': self._id}, self._fields, upsert=True)
            else:
                self._fields['_id'] = self.insert_one(
                    self._fields, serialized=False
                )

            return self.get('_id', serialized)
        else:
            return self.errors(serialized)
