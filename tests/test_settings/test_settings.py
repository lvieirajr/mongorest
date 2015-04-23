# -*- encoding: UTF-8 -*-

from os import environ

from mongorest.settings import Settings
from mongorest.testcase import TestCase


class TestSettings(TestCase):

    def test_settings_has_default_values_for_database(self):
        settings = Settings()

        self.assertIsNotNone(settings.DATABASE)
        self.assertEqual(settings.DATABASE['HOST'], 'localhost')
        self.assertEqual(settings.DATABASE['PORT'], 27017)
        self.assertEqual(settings.DATABASE['NAME'], 'mongorest')
        self.assertEqual(settings.DATABASE['USER'], '')
        self.assertEqual(settings.DATABASE['PASSWORD'], '')

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
