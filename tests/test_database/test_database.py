# -*- encoding: UTF-8 -*-

from pymongo import MongoClient
from pymongo.database import Database

from mongorest.database import _get_db
from mongorest.settings import settings
from mongorest.testcase import TestCase


class TestDatabase(TestCase):

    def test__get_db_returns_database_with_correct_host(self):
        self.assertEqual(_get_db().client.HOST, 'localhost')

    def test__get_db_returns_database_with_correct_port(self):
        self.assertEqual(_get_db().client.PORT, 27017)

    def test__get_db_returns_database_with_correct_name(self):
        self.assertEqual(_get_db().name, 'mongorest')

    def test__get_db_returns_database_if_no_user(self):
        self.assertIsInstance(_get_db(), Database)

    def test__get_db_returns_database_if_authenticate(self):
        database = settings.DATABASE
        db = MongoClient(database['HOST'], database['PORT'])[database['NAME']]
        db.add_user('test', 'test', roles=['read'])

        database['USER'] = 'test'
        database['PASSWORD'] = 'test'

        self.assertIsInstance(_get_db(), Database)

        database['USER'] = ''
        database['PASSWORD'] = ''

    def test__get_db_raises_exception_if_user_and_not_authenticated(self):
        database = settings.DATABASE
        db = MongoClient(database['HOST'], database['PORT'])[database['NAME']]
        db.add_user('test', 'test', roles=['read'])

        database['USER'] = 'test'
        database['PASSWORD'] = 'not_test'

        with self.assertRaises(Exception):
            _get_db()

        database['USER'] = ''
        database['PASSWORD'] = ''
