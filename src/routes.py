import jsonschema
import uuid

from flask import Flask, request, abort
from flask_restful import Resource, Api
from loguru import logger

from . import cache, db, tasks


todo_schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'},
        'text': {'type': 'string'},
        'completed': {'type': 'boolean'}
    },
    'additionalProperties': False
}


def _default_to(json: dict, key: str, value):
    if not key in json:
        json[key] = value


def validate_todo(json_body):
    _default_to(json_body, 'id', str(uuid.uuid4()))
    _default_to(json_body, 'completed', False)
    jsonschema.validate(instance=json_body, schema=todo_schema)


class TodoAll(Resource):

    def get(self):
        keys = db.list_todos()
        return list(keys)

    def post(self):
        body = request.get_json()
        validate_todo(body)
        tasks.get_queue().enqueue(tasks.add_todo_to_db, body)
        return body['id'], 202


class TodoSingle(Resource):

    def get(self, todo_id: str):
        x = cache.get_todo(todo_id, db.get_todo)
        if x is None:
            return abort(404)
        return x, 200

    def post(self, todo_id: str):
        body = request.get_json()
        body['id'] = todo_id
        validate_todo(body)
        tasks.get_queue().enqueue(tasks.add_todo_to_db, body)
        return todo_id, 202

    def delete(self, todo_id: str):
        tasks.get_queue().enqueue(tasks.delete_todo_from_cache, todo_id)
        tasks.get_queue().enqueue(tasks.delete_todo_from_db, todo_id)
        return todo_id, 202


class HelloWorld(Resource):

    def __init__(self, **kwargs):
        self.message = kwargs.get('message', 'Hello, World!')

    def get(self):
        message = self.message.split(' ')
        return message


def create_routes(app: Flask) -> Flask:
    app.logger.info('Registering routes')

    api = Api(app)
    api.add_resource(
        HelloWorld,
        '/hello',
        resource_class_kwargs={
            'message': app.config.message
        }
    )

    api.add_resource(TodoAll, '/todo')
    api.add_resource(TodoSingle, '/todo/<string:todo_id>')

    app.logger.info('Registered "/hello"')

    return app
