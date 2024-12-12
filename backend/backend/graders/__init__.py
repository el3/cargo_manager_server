from .fish import start_fish_grader_tasks
from flask import Blueprint, current_app, session
from flask_httpauth import HTTPBasicAuth
from werkzeug.exceptions import BadRequest, NotFound
import trio

api = Blueprint('graders', __name__)
auth = HTTPBasicAuth(scheme='BasicAPI')
error_messages = {
    401: 'unauthorized',
    403: 'forbidden',
}


@api.errorhandler(BadRequest)
@api.errorhandler(NotFound)
def bad_request(error):
    return {'message': error.description}, error.code


@auth.error_handler
def error_handler(status_code):
    return {
        'message': error_messages.get(status_code, 'unknown_error')
    }, status_code


@auth.verify_password
def verify_password(username, password):
    if session.get('admin'):
        return 'admin'

    admin_password = current_app.config['ADMIN_PASSWORD']

    if (
        username == 'admin'
        and password == admin_password
    ):
        session['admin'] = True
        return 'admin'


@api.cli.command()
def start_socket_tasks() -> None:
    """CLI command to start the fish grader tasks with Trio."""
    print('Starting socket tasks...')
    print(f"Current app name: {current_app.name}")

    trio.run(start_fish_grader_tasks)