# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from os import environ

from mongorest.database import db, _get_db, AutoReconnectProxy
from mongorest.testcase import TestCase


class TestDatabase(TestCase):

    def test_db_is_a_proxied_pymongo_database(self):
        self.assertIsInstance(db, AutoReconnectProxy)

    def test_db_connected_to_correct_database(self):
        self.assertEqual(db.name, 'mongorest')

    def test_correct_db_when_uri_passed(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.fixtures.database_test_uri_settings'
        database = _get_db()

        self.assertEqual(database.client.HOST, 'localhost')
        self.assertEqual(database.client.PORT, 27017)
        self.assertEqual(database.name, 'mongorest-test')

    def test_correct_db_when_host_and_port_passed(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.fixtures.database_test_host_port_settings'
        database = _get_db()

        self.assertEqual(database.client.HOST, 'localhost')
        self.assertEqual(database.client.PORT, 27017)
        self.assertEqual(database.name, 'mongorest-test')

    def test_correct_db_when_hosts_and_ports_passed(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.fixtures.database_test_hosts_ports_settings'
        database = _get_db()

        self.assertEqual(database.client.HOST, 'localhost')
        self.assertEqual(database.client.PORT, 27017)
        self.assertEqual(database.name, 'mongorest-test')
