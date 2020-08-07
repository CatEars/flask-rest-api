import json
import redis
from flask import Flask
from loguru import logger

client = None
expire_time = None


def get_client():
    return client


def get_expire_time():
    return expire_time


def get_todo(todo_id: str, retrieval_func):
    client = get_client()
    logger.info(f'Getting todo {todo_id} from cache')
    key = f'todo-{todo_id}'
    if client.exists(key):
        logger.debug(f'Cache hit for {todo_id}')
        return json.loads(client.get(key))

    logger.debug(f'Cache miss for {todo_id}')
    result = retrieval_func(todo_id)
    if result:
        with client.pipeline() as pipe:
            pipe.set(key, json.dumps(result))
            pipe.expire(key, get_expire_time())
            pipe.execute()
    return result


def delete_todo(todo_id: str):
    client = get_client()
    logger.info(f'Deleting todo {todo_id} from cache')
    key = f'todo-{todo_id}'
    res = client.delete(key)
    if res == 0:
        return None
    return todo_id


def initialize_cache(app: Flask):
    global client, expire_time

    host = app.config.REDIS_HOST
    port = app.config.REDIS_PORT
    expire_time = app.config.get('EXPIRE_TIME', 3600)

    client = redis.Redis(host=host, port=port)
