# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from os import environ

from mongorest.settings import Settings
from mongorest.testcase import TestCase


class TestSettings(TestCase):

    def test_settings_has_default_values_for_database(self):
        settings = Settings()

        self.assertIsNotNone(settings.MONGODB)
        self.assertEqual(settings.MONGODB['URI'], '')
        self.assertEqual(settings.MONGODB['USERNAME'], '')
        self.assertEqual(settings.MONGODB['PASSWORD'], '')
        self.assertEqual(settings.MONGODB['HOSTS'], ['localhost'])
        self.assertEqual(settings.MONGODB['PORTS'], [27017])
        self.assertEqual(settings.MONGODB['DATABASE'], 'mongorest')
        self.assertEqual(settings.MONGODB['OPTIONS'], [])

    def test_settings_has_default_value_true_for_serialize(self):
        environ.pop('MONGOREST_SETTINGS_MODULE')
        settings = Settings()

        self.assertTrue(settings.SERIALIZE)

    def test_a_default_setting_can_be_overwritten(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.test_settings.fixtures.settings'
        settings = Settings()

        self.assertFalse(settings.SERIALIZE)

    def test_a_new_setting_value_can_be_added(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.test_settings.fixtures.settings'
        settings = Settings()

        self.assertEqual(settings.TEST_VALUE, 'test')
