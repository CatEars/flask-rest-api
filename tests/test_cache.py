import json
import pytest
import redis

from src import cache
from .mocks import FakeRedisClient, FakeFlaskApp


@pytest.fixture
def fake_redis(monkeypatch):
    client = FakeRedisClient()
    monkeypatch.setattr(cache, 'get_client', lambda: client)
    return client


def test_retrieve_cached_todo(fake_redis):
    fake_redis._add('todo-123', json.dumps({'message': 'wowz'}))

    res = cache.get_todo('123', lambda x: None)

    assert 'message' in res
    assert res['message'] == 'wowz'


def test_retrieve_non_existing_todo(fake_redis):
    res = cache.get_todo('123', lambda x: None)
    assert res is None


def test_retrieve_existing_todo(fake_redis):
    res = cache.get_todo('123', lambda x: {'message': 'wowz'})

    assert 'message' in res
    assert res['message'] == 'wowz'


def test_delete_existing_todo(fake_redis):
    fake_redis._add('todo-123', json.dumps({'message': 'wowz'}))
    todo_id = cache.delete_todo('123')
    assert todo_id == '123'


def test_delet_non_existing_todo(fake_redis):
    todo_id = cache.delete_todo('123')
    assert todo_id is None


def test_initiaize(monkeypatch):
    monkeypatch.setattr(redis, 'Redis', FakeRedisClient)

    cache.initialize_cache(FakeFlaskApp())
    assert isinstance(cache.get_expire_time(), int)
    assert isinstance(cache.get_client(), FakeRedisClient)
