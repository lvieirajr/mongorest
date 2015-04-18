# -*- encoding: UTF-8 -*-

from mongorest.database import db
from mongorest.utils import serialize

__all__ = [
    'Collection',
]


class CollectionMeta(type):
    """
    MetaClass for the Collection Class.
    Prepares the member dict adding the correct collection based on the name,
    And adds the required_fields dict.
    """
    @classmethod
    def __prepare__(mcs, name, bases):
        """
        Returns the collection based on the name of the Class
        Also an empty required_fields dict to serve as a base
        """
        return {
            'collection': db[name.lower()],
            'required_fields': {},
        }


class Collection(object, metaclass=CollectionMeta):
    """
    Base class for Collections.
    Can Serialize and De-Serialize the data.
    """
    def __new__(cls, *args, **kwargs):
        import ipdb; ipdb.set_trace()
        return Document(cls, *args, **kwargs)

    @classmethod
    def find_one(cls, filter=None, serialized=False):
        document = cls.collection.find_one(filter)
        return serialize(document) if serialized else document

    @classmethod
    def find(cls, filter=None, serialized=False):
        documents = list(cls.collection.find(filter))
        return serialize(documents) if serialized else documents

    @classmethod
    def aggregate(cls, pipeline, serialized=False):
        documents = list(cls.collection.aggregate(pipeline))
        return serialize(documents) if serialized else documents

    @classmethod
    def insert_one(cls, document, serialized=False):
        _id = cls.collection.insert_one(document).inserted_id
        return serialize(_id) if serialized else _id

    @classmethod
    def insert_many(cls, documents, ordered=True, serialized=False):
        _ids = cls.collection.insert_many(documents, ordered).inserted_ids
        return serialize(_ids) if serialized else _ids

    @classmethod
    def update_one(cls, filter, update, upsert=False, serialized=False):
        updated = cls.collection.udpate_one(filter, update, upsert).raw_result
        return serialize(updated) if serialized else updated

    @classmethod
    def update_many(cls, filter, update, upsert=False, serialized=False):
        updated = cls.collection.udpate_many(filter, update, upsert).raw_result
        return serialize(updated) if serialized else updated

    @classmethod
    def delete_one(cls, filter, serialized=False):
        deleted = cls.collection.delete_one(filter).raw_result
        return serialize(deleted) if serialized else deleted

    @classmethod
    def delete_many(cls, filter, serialized=False):
        deleted = cls.collection.delete_many(filter).raw_result
        return serialize(deleted) if serialized else deleted

    @classmethod
    def count(cls, filter=None):
        return len(cls.find(filter))

    @classmethod
    def get(cls, filter=None):
        document = Document(cls=cls, fields=cls.find_one(filter))
        return document if document.pk else None


class Document(object):
    """
    Document Class
    It will know how to validate its fields
    Will use the required_fields of the Collection to do so.
    """

    def __init__(self, cls, fields=None, errors=None):
        super(Document, self).__init__()

        self._cls = cls
        self._fields = fields or {}
        self._errors = errors or {}

        self._validate()

    def __getattr__(self, attr):
        if attr in ('_cls', '_fields', '_errors'):
            return object.__getattribute__(self, attr)
        elif attr in self._fields:
            return self._fields[attr]
        elif hasattr(self._cls, attr):
            return object.__getattribute__(self._cls, attr)
        else:
            return object.__getattribute__(self, attr)

    def __setattr__(self, attr, value):
        if attr in ('_cls', '_fields', '_errors'):
            object.__setattr__(self, attr, value)
        else:
            self._fields[attr] = value

    def _validate(self):
        """
        Validates if the required fields are present on the Document
        Validates if the required fields are of the correct types
        If one of these two validations fail, add an error to self._errors
        """
        for (field, type_or_tuple) in self.required_fields.items():
            if field in self._fields:
                if not isinstance(self._fields[field], type_or_tuple):
                    types = type_or_tuple

                    if hasattr(type_or_tuple, '__iter__'):
                        types = ' or '.join([t.__name__ for t in type_or_tuple])

                    self.errors[field] = 'Field \'{}\' must be of type(s): {}.'.format(
                        field, types
                    )
            else:
                self.errors[field] = 'Field \'{}\' is required.'.format(field)

    def save(self):
        pass

    @property
    def is_valid(self):
        return len(self._errors) == 0

    @property
    def pk(self):
        return self._fields.get('_id')
