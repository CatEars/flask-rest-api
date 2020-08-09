from dynaconf import Dynaconf
import pymongo
import redis
from rq import Queue
from flask import Flask
from loguru import logger

queue = None

def get_queue():
    return queue


def get_config():
    return Dynaconf(
        settings_files=['settings.toml']
    ).default


def get_mongo_db():
    config = get_config()
    return pymongo.MongoClient(
        host=config.MONGO_HOST,
        port=config.MONGO_PORT
    )[config.MONGO_DB_NAME]


def get_redis_client():
    config = get_config()
    return redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT
    )


def add_todo_to_db(todo):
    logger.info('Adding todo to DB')
    db = get_mongo_db()
    todo['_id'] = todo['id']
    del todo['id']

    db.todos.insert_one(todo)
    return todo['_id']


def delete_todo_from_db(todo_id: str):
    logger.info('deleting todo from DB')
    get_mongo_db().todos.delete_one({'_id': todo_id})


def delete_todo_from_cache(todo_id: str):
    logger.info('deleting todo from cache')
    client = get_redis_client()
    client.delete(f'todo-{todo_id}')


def initialize_tasks(app: Flask):
    global queue

    host = app.config.REDIS_HOST
    port = app.config.REDIS_PORT

    queue = Queue(connection=redis.Redis(host, port))
