#!/usr/bin/python3
""" city REST API module definition """
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
        "Amenity": Amenity,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User
        }


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def retrieve_city_place(city_id):
    """ retrieve all place objects of a city id connection """
    dictionary = {}
    dictionary = storage.get(classes['City'], city_id)
    all_list = []
    if dictionary:
        for key in dictionary.places:
            all_list.append(key.to_dict())
    elif not dictionary:
        abort(404)
    return jsonify(all_list)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def retrive_place(place_id):
    """ retrieving place objects according to place id """
    place_object = storage.get(classes['Place'], place_id)
    if not place_object:
        abort(404)
    if place_object:
        return jsonify(place_object.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def deleting_place(place_id):
    """ method to delete place objects according to place id """
    place_object = storage.get(classes['Place'], place_id)
    if not place_object:
        abort(404)
    elif place_object:
        storage.delete(place_object)
        storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def posting_place_method(city_id):
    """ posting place object """
    place = request.get_json()
    city = storage.get(classes['City'], city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    if 'name' not in place:
        abort(400, description='Missing name')
    if 'user_id' not in request.get_json():
        abort(400, description='Missing user_id')
    user = storage.get(classes['User'], place['user_id'])
    if not user:
        abort(404)
    instance_place = classes['Place'](**place)
    instance_place.city_id = city.id
    instance_place.user_id = user.id
    instance_place.save()
    return jsonify(instance_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def put_place_method(place_id):
    """ put place object into the database """
    request_body = request.get_json()
    place_object = storage.get(classes['Place'], place_id)
    if not request_body:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    ignore_list = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for keys, values in request_body.items():
        if keys not in ignore_list:
            setattr(place_object, keys, values)
    storage.save()
    return jsonify(place_object.to_dict()), 200
