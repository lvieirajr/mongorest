# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from os import environ
from pymongo.database import Database

from mongorest.database import db, _get_db
from mongorest.testcase import TestCase


class TestDatabase(TestCase):

    def test_db_is_a_pymongo_database(self):
        self.assertIsInstance(db, Database)

    def test_db_connected_to_correct_database(self):
        self.assertEqual(db.name, 'mongorest')

    def test_correct_db_when_uri_passed(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.test_database.fixtures.uri'
        database = _get_db()

        self.assertEqual(database.client.HOST, 'localhost')
        self.assertEqual(database.client.PORT, 27017)
        self.assertEqual(database.name, 'mongorest-test')

    def test_correct_db_when_host_and_port_passed(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.test_database.fixtures.host_port'
        database = _get_db()

        self.assertEqual(database.client.HOST, 'localhost')
        self.assertEqual(database.client.PORT, 27017)
        self.assertEqual(database.name, 'mongorest-test')

    def test_correct_db_when_hosts_and_ports_passed(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'tests.test_database.fixtures.hosts_ports'
        database = _get_db()

        self.assertEqual(database.client.HOST, 'localhost')
        self.assertEqual(database.client.PORT, 27017)
        self.assertEqual(database.name, 'mongorest-test')
