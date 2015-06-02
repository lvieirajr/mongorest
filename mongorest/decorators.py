# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from functools import wraps
from werkzeug.wrappers import Response

from .settings import settings
from .utils import serialize

__all__ = [
    'ensure_indexes',
    'login_required',
    'serializable',
]


def ensure_indexes(wrapped):
    """
    Calls the 'indexes' function from the class of the wrapped function
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


def login_required(wrapped):
    """
    Requires that the user is logged in and authorized to execute requests
    Except if the method is in authorized_methods of the auth_collection
    Then he can execute the requests even not being authorized
    """
    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        request = args[1]
        method = request.method

        auth_collection = request.environ.get(
            settings.AUTH_COLLECTION[
                settings.AUTH_COLLECTION.rfind('.') + 1:
            ].lower()
        )

        if auth_collection:
            authorized_methods = []

            if hasattr(auth_collection, 'authorized_methods'):
                authorized_methods = auth_collection.authorized_methods()

            if auth_collection.is_authorized() or method in authorized_methods:
                return wrapped(*args, **kwargs)

        return Response(
            serialize({'unauthorized': 'Unauthorized.'}),
            content_type='application/json',
            status=401,
        )

    if hasattr(wrapped, 'decorators'):
        wrapper.decorators = wrapped.decorators
        wrapper.decorators.append('login_required')
    else:
        wrapper.decorators = ['login_required']

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
