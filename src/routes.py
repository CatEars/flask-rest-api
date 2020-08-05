from flask import Flask
from flask_restful import Resource, Api

class HelloWorld(Resource):

    def get(self):
        return {'Hello': 'World!'}

def create_routes(app: Flask) -> Flask:

    api = Api(app)
    api.add_resource(HelloWorld, '/hello')

    return app
