#!/usr/bin/python3
"""
index
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """ return Status """
    data = {
        "status": "OK"
    }
    resp = jsonify(data)
    return resp


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def statistics():
    """ method to return count in dictionary form """
    response = {}
    response['amenities'] = storage.count(Amenity)
    response['cities'] = storage.count(City)
    response['places'] = storage.count(Place)
    response['reviews'] = storage.count(Review)
    response['states'] = storage.count(State)
    response['users'] = storage.count(User)
    return jsonify(response)
