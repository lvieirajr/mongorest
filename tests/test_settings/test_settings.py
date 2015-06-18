# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from os import environ

from mongorest.settings import settings
from mongorest.testcase import TestCase


class TestSettings(TestCase):

    def test_settings_default_values(self):
        environ.pop('MONGOREST_SETTINGS_MODULE', None)

        self.assertEqual(settings.AUTH_COLLECTION, '')

        self.assertIsNotNone(settings.CORS)
        self.assertEqual(
            settings.CORS['Access-Control-Allow-Origin'],
            '*'
        )
        self.assertEqual(
            settings.CORS['Access-Control-Allow-Methods'],
            'GET,POST,PUT,PATCH,DELETE,OPTIONS'
        )
        self.assertEqual(
            settings.CORS['Access-Control-Allow-Headers'],
            'Accept,Accept-Encoding,Authorization,Content-Length,Content-Type,'
            'Origin,User-Agent,X-CSRFToken,X-Requested-With'
        )
        self.assertEqual(
            settings.CORS['Access-Control-Allow-Credentials'], 'true'
        )

        self.assertEqual(settings.DOMAIN, '127.0.0.1')

        self.assertEqual(settings.MIDDLEWARES, [])

        self.assertIsNotNone(settings.MONGODB)
        self.assertEqual(settings.MONGODB['URI'], '')
        self.assertEqual(settings.MONGODB['USERNAME'], '')
        self.assertEqual(settings.MONGODB['PASSWORD'], '')
        self.assertEqual(settings.MONGODB['HOST'], 'localhost')
        self.assertEqual(settings.MONGODB['HOSTS'], [])
        self.assertEqual(settings.MONGODB['PORT'], 27017)
        self.assertEqual(settings.MONGODB['PORTS'], [])
        self.assertEqual(settings.MONGODB['DATABASE'], 'mongorest')
        self.assertEqual(settings.MONGODB['OPTIONS'], [])

        self.assertEqual(settings.SESSION_STORE, '')

    def test_a_default_setting_can_be_overwritten(self):
        environ.pop('MONGOREST_SETTINGS_MODULE', None)

        self.assertEqual(settings.MONGODB['URI'], '')

        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.fixtures.settings_test_settings'

        self.assertEqual(settings.MONGODB['URI'], 'test')

    def test_a_new_setting_value_can_be_added(self):
        environ.pop('MONGOREST_SETTINGS_MODULE', None)
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.fixtures.settings_test_settings'

        self.assertEqual(settings.TEST, 'test')

    def test_an_invalid_setting_will_raise_error(self):
        environ.pop('MONGOREST_SETTINGS_MODULE', None)

        with self.assertRaises(AttributeError):
            return settings.i_am_an_invalid_setting
