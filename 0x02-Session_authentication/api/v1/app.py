#!/usr/bin/env python3
"""
    Module for Route of the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

if os.getenv("AUTH_TYPE") == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()

elif os.getenv("AUTH_TYPE") == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()

elif getenv('AUTH_TYPE') == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif getenv('AUTH_TYPE') == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif getenv('AUTH_TYPE') == 'session_db_auth':
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Method to handle 'Not found' error
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """
    Unauthorized handler method
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """
    Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> str:
    """
    Mehtod to filter request
    """
    request_path_list = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/']
    if auth:
        if auth.require_auth(request.path, request_path_list):
            if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
                abort(401)
            if auth.current_user(request) is None:
                abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
