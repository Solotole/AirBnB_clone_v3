#!/usr/bin/python3
"""
index
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """ return Status """
    data = {
        "status": "OK"
    }
    resp = jsonify(data)
    return resp
