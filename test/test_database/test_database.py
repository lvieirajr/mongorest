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

    def test_db_connected_to_correct_node_when_host_and_port_passed(self):
        self.assertEqual(db.client.HOST, 'localhost')
        self.assertEqual(db.client.PORT, 27017)

    def test_db_connected_to_correct_nodes_when_hosts_and_ports_passed(self):
        environ['MONGOREST_SETTINGS_MODULE'] = 'test.test_database.fixtures.settings'
        database = _get_db()
        self.assertEqual(database.client.HOST, 'localhost')
        self.assertEqual(database.client.PORT, 27017)
