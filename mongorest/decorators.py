# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from functools import wraps

from .utils import serialize

__all__ = [
    'ensure_indexes',
    'serializable',
]


def ensure_indexes(wrapped):
    """
    If a keyword argument 'serialize' with a True value is passed to the
    Wrapped function, the return of the wrapped function will be serialized.
    Nothing happens if the argument is not passed or the value is not True
    """

    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        if hasattr(args[0], 'indexes'):
            args[0].indexes()

        return wrapped(*args, **kwargs)

    if hasattr(wrapped, 'decorators'):
        wrapper.decorators = wrapped.decorators
        wrapper.decorators.append('ensure_indexes')
    else:
        wrapper.decorators = ['ensure_indexes']

    return wrapper


def serializable(wrapped):
    """
    If a keyword argument 'serialize' with a True value is passed to the
    Wrapped function, the return of the wrapped function will be serialized.
    Nothing happens if the argument is not passed or the value is not True
    """

    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        should_serialize = kwargs.pop('serialize', False)
        result = wrapped(*args, **kwargs)

        return serialize(result) if should_serialize else result

    if hasattr(wrapped, 'decorators'):
        wrapper.decorators = wrapped.decorators
        wrapper.decorators.append('serializable')
    else:
        wrapper.decorators = ['serializable']

    return wrapper
