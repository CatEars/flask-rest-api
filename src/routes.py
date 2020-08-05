from flask import Flask
from flask_restful import Resource, Api


class HelloWorld(Resource):

    def __init__(self, **kwargs):
        self.message = kwargs.get('message', 'Hello, World!')

    def get(self):
        message = self.message.split(' ')
        return message


def create_routes(app: Flask) -> Flask:

    api = Api(app)
    api.add_resource(
        HelloWorld,
        '/hello',
        resource_class_kwargs={
            'message': app.config.message
        }
    )

    return app
