import json
import dynaconf
import pymongo
import redis
import pytest

from src import tasks
from .mocks import FakeRedisClient, FakeFlaskApp, FakeMongoClient


@pytest.fixture
def fake_redis(monkeypatch):
    monkeypatch.setattr(redis, 'Redis', FakeRedisClient)
    client = FakeRedisClient()
    client._clear()
    return client


@pytest.fixture
def app_config():
    return dynaconf.Dynaconf(settings_files=['settings.toml']).default


@pytest.fixture
def fake_mongo(monkeypatch, app_config):
    client = FakeMongoClient()
    client[app_config.MONGO_DB_NAME]._add_table('todos')
    monkeypatch.setattr(pymongo, 'MongoClient', FakeMongoClient)
    return client[app_config.MONGO_DB_NAME]


def test_add_todo_to_db(fake_mongo):
    my_todo = {
        'id': '123',
        'message': 'abc',
        'completed': False
    }
    todo_id = tasks.add_todo_to_db(my_todo)
    assert todo_id == '123'
    assert fake_mongo.todos.find_one({'_id': '123'})['_id'] == '123'
    assert fake_mongo.todos.find_one({'_id': '123'})['message'] == 'abc'
    assert fake_mongo.todos.find_one({'_id': '123'})['completed'] == False


def test_delete_todo_from_db(fake_mongo):
    my_todo = {
        'id': '123',
        'message': 'abc',
        'completed': False
    }
    todo_id = tasks.add_todo_to_db(my_todo)
    assert todo_id == '123'
    tasks.delete_todo_from_db(todo_id)
    assert fake_mongo.todos.find_one({'_id': '123'}) is None


def test_delete_todo_from_cache(fake_redis):
    my_todo = {
        'id': '123',
        'message': 'abc',
        'completed': False
    }
    fake_redis.set('todo-123', json.dumps(my_todo))
    assert fake_redis.exists('todo-123')
    tasks.delete_todo_from_cache('123')
    assert not fake_redis.exists('todo-123')

