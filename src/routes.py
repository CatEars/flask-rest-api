import jsonschema
import uuid

from flask import Flask, request, abort
from flask_restful import Resource, Api
from loguru import logger

todos = {}

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

def add_todo(json_body) -> str:
    _default_to(json_body, 'id', str(uuid.uuid4()))
    _default_to(json_body, 'completed', False)
    jsonschema.validate(instance=json_body, schema=todo_schema)

    todos[json_body['id']] = json_body
    return json_body['id']


def get_todo(todo_id: str):
    return todos.get(todo_id)


def delete_todo(todo_id: str):
    if not todo_id in todos:
        return None
    del todos[todo_id]
    return todo_id


class HelloWorld(Resource):

    def __init__(self, **kwargs):
        self.message = kwargs.get('message', 'Hello, World!')

    def get(self):
        message = self.message.split(' ')
        return message


class TodoAll(Resource):

    def get(self):
        keys = todos.keys()
        return list(keys)

    def post(self):
        return add_todo(request.get_json()), 201


class TodoSingle(Resource):

    def get(self, todo_id: str):
        logger.info(f'Returning TODO "{todo_id}"')
        x = get_todo(todo_id)
        if x is None:
            return abort(404)
        return x, 200

    def post(self, todo_id: str):
        body = request.get_json()
        body['id'] = todo_id
        todo_id = add_todo(body)
        return todo_id, 201

    def delete(self, todo_id: str):
        res = delete_todo(todo_id)
        if res is None:
            return abort(404)
        return res, 202


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
