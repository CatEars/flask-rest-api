import pymongo

from flask import Flask
from loguru import logger

client = None
db = None


def get_db():
    return db


def list_todos():
    db = get_db()
    return [
        str(todo_id) for todo_id in db.todos.find().distinct('_id')
    ]


def get_todo(todo_id: str):
    db = get_db()
    logger.info(f'Getting todo {todo_id} from mongo')
    res = db.todos.find_one({'_id': todo_id})
    if res is None:
        return None

    res['id'] = res['_id']
    del res['_id']
    return res


def initialize_db(app: Flask):
    global client, db

    host = app.config.MONGO_HOST
    port = app.config.MONGO_PORT
    dbname = app.config.MONGO_DB_NAME

    logger.info(f'Initializing mongo database {host}:{port}/{dbname}')
    client = pymongo.MongoClient(host, port)
    db = client[dbname]
