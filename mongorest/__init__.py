# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import os

if os.environ.get('MONGOREST_SETTINGS_MODULE'):
    from .collection import Collection
    from .wrappers import Request, Response
    from .utils import deserialize, serialize

__version__ = '3.2.0'
