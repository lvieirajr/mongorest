# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

try:
    import unittest2 as unittest
except:
    import unittest


if __name__ == '__main__':
    unittest.TextTestRunner().run(
        unittest.defaultTestLoader.loadTestsFromName('test')
    )
