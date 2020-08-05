from flask import Flask

def create_routes(app: Flask) -> Flask:

    @app.route('/hello')
    def hello_world():
        return 'Hello, World!\n'

    return app
