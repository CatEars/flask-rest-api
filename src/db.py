from flask import Flask
from pymongo import MongoClient
from loguru import logger

client = None
db = None


def list_todos():
    return [
        str(todo_id) for todo_id in db.todos.find().distinct('_id')
    ]


def add_todo(todo):
    logger.info(f'Adding todo {todo["id"]} to mongo')
    todo['_id'] = todo['id']
    del todo['id']

    db.todos.insert_one(todo)
    return todo['_id']


def get_todo(todo_id: str):
    logger.info(f'Getting todo {todo_id} from mongo')
    res = db.todos.find_one({'_id': todo_id})
    if res is None:
        return None

    res['id'] = res['_id']
    del res['_id']
    return res


def delete_todo(todo_id: str):
    logger.info(f'Deleting todo {todo_id} in mongo')
    res = db.todos.delete_one({'_id': todo_id})
    if res.deleted_count == 1:
        return todo_id
    else:
        return None


def initialize_db(app: Flask):
    global client, db

    host = app.config.MONGO_HOST
    port = app.config.MONGO_PORT
    dbname = app.config.MONGO_DB_NAME

    logger.info(f'Initializing mongo database {host}:{port}/{dbname}')
    client = MongoClient(host, port)
    db = client[dbname]
