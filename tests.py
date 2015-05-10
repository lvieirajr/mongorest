# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

try:
    import unittest2 as unittest
except ImportError:
    import unittest


__all__ = [
    'run_tests'
]


def run_tests():
    result = unittest.TextTestRunner().run(
        unittest.defaultTestLoader.loadTestsFromName('test')
    )

    return not bool(result.failures + result.errors)


if __name__ == '__main__':
    run_tests()