# -*- encoding: UTF-8 -*-

from pymongo.database import Database

from mongorest.database import db
from mongorest.testcase import TestCase


class TestDatabase(TestCase):

    def test_db_is_a_pymongo_database(self):
        self.assertIsInstance(db, Database)

    def test_db_connected_to_correct_nodes(self):
        self.assertEqual(set(db.client.nodes), {('localhost', 27017)})

    def test_db_connected_to_correct_database(self):
        self.assertEqual(db.name, 'mongorest')
