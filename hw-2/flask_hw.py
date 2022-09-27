import json
from enum import Enum, unique

from flask import Flask, Response, request
from werkzeug.exceptions import HTTPException


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    storage = dict()

    @unique
    class CONTENT_TYPE(str, Enum):
        TEXT_PLAIN = 'text/plain'
        APP_JSON = 'application/json'

    @app.route('/hello', methods=['GET'])
    def hello():
        return Response('HSE OneLove!', mimetype=CONTENT_TYPE.TEXT_PLAIN, status=200)

    @app.route('/set', methods=['POST'])
    def _set():
        if request.content_type != CONTENT_TYPE.APP_JSON:
            return Response(status=415)
        content = json.loads(request.data)
        if 'key' not in content or 'value' not in content:
            return Response(status=400)
        storage[content['key']] = content['value']
        return Response(status=200)

    @app.route('/get/<key>', methods=['GET'])
    def get(key):
        if key not in storage:
            return Response(status=404)
        return Response(
            response=json.dumps({'key': key, 'value': storage['key']}),
            status=200,
            content_type=CONTENT_TYPE.APP_JSON,
        )

    @app.route('/divide', methods=['POST'])
    def divide():
        if request.content_type != CONTENT_TYPE.APP_JSON:
            return Response(status=415)
        content = json.loads(request.data)
        if 'dividend' not in content or 'divider' not in content:
            return Response(status=400)
        try:
            res = str(int(content['dividend']) / int(content['divider']))
            return Response(
                response=res,
                status=200,
                content_type=CONTENT_TYPE.TEXT_PLAIN,
            )
        except Exception:
            return Response(
                status=400,
            )

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        return Response(status=405)

    return app


if __name__ == '__main__':
    create_app().run()
