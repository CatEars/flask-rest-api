import pytest
import pymongo

from .mocks import FakeMongoDb, FakeFlaskApp, FakeMongoClient
from src import db


@pytest.fixture
def fake_mongo(monkeypatch):
    mongo = FakeMongoDb()
    mongo._add_table('todos')
    monkeypatch.setattr(db, 'get_db', lambda: mongo)
    return mongo


def test_list_todos_empty(fake_mongo):
    assert len(db.list_todos()) == 0


def test_list_with_single_todo(fake_mongo):
    fake_mongo.todos._add({'_id': '123', 'message': 'wowzers'})
    assert db.list_todos() == ['123']


def test_get_non_existant_todo(fake_mongo):
    assert db.get_todo('123') is None


def test_get_existing_todo(fake_mongo):
    fake_mongo.todos._add({'_id': '123', 'message': 'wowzers'})
    todo = db.get_todo('123')
    assert todo is not None

    assert todo['id'] == '123'
    assert todo['message'] == 'wowzers'


def test_initialize(monkeypatch):
    monkeypatch.setattr(pymongo, 'MongoClient', FakeMongoClient)
    db.initialize_db(FakeFlaskApp())
    assert isinstance(db.get_db(), FakeMongoDb)
