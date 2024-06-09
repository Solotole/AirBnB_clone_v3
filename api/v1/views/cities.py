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


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def retrieve_city_state(state_id):
    """ retrieve all city objects of a state connection """
    dictionary = {}
    dictionary = storage.get(classes['State'], state_id)
    all_list = []
    if dictionary:
        for key in dictionary.cities:
            all_list.append(key.to_dict())
    elif not dictionary:
        abort(404)
    return jsonify(all_list)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def retrive_city(city_id):
    """ retrieving city objects according to city id """
    dictionary_c = storage.get(classes['City'], city_id)
    if not dictionary_c:
        abort(404)
    if dictionary_c:
        return jsonify(dictionary_c.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def deleting_city(city_id):
    """ method to delete coty objects according to city id """
    dictionary_c = storage.get(classes['City'], city_id)
    if not dictionary_c:
        abort(404)
    elif dictionary_c:
        storage.delete(dictionary_c)
        storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def posting_city(state_id):
    """ posting city object """
    dict_object = request.get_json()
    dictionary = storage.get(classes['State'], state_id)
    if not dictionary:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    if 'name' not in dict_object:
        abort(400, description='Missing name')
    instance_one = classes['City'](**dict_object)
    instance_one.state_id = dictionary.id
    instance_one.save()
    return jsonify(instance_one.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def putting_method(city_id):
    """ put city object into the database """
    dict_object = request.get_json()
    dictionary_c = storage.get(classes['City'], city_id)
    if not dictionary_c:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    ignore_list = ['id', 'state_id', 'created_at', 'updated_at']
    for keys, values in dict_object.items():
        if keys not in ignore_list:
            setattr(dictionary_c, keys, values)
    storage.save()
    return jsonify(dictionary_c.to_dict()), 200
