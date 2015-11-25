# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from functools import wraps
from werkzeug.wrappers import Response

from .errors import UnauthorizedError
from .settings import settings
from .utils import serialize

__all__ = [
    'login_required',
    'serializable',
]


def login_required(wrapped):
    """
    Requires that the user is logged in and authorized to execute requests
    Except if the method is in authorized_methods of the auth_collection
    Then he can execute the requests even not being authorized
    """
    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        request = args[1]

        auth_collection = settings.AUTH_COLLECTION[
            settings.AUTH_COLLECTION.rfind('.') + 1:
        ].lower()
        auth_document = request.environ.get(auth_collection)

        if auth_document and auth_document.is_authorized(request):
            setattr(request, auth_collection, auth_document)
            return wrapped(*args, **kwargs)

        return Response(
            response=serialize(UnauthorizedError()),
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
