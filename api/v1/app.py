#!/usr/bin/python3

"""
create app file that runs
and handles other functions
"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    teardown function
    """
    storage.close()


@app.errorhandler(404)
def error(e):
    """handle 404 error"""
    return make_response({"error": "Not found"}, 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if not host:
        host = 'localhost'
    if not port:
        port = '0.0.0.0'
    app.run(host=host, port=port, threaded=True)
