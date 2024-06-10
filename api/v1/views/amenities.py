#!/usr/bin/python3
"""module defining routes for amenity class"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

classes = {"Amenity": Amenity}


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def getting_all_objects():
    """ getting a list of all objects """
    dict_amenity = {}
    dict_amenity = storage.all(classes['Amenity'])
    all_amenity = []
    if dict_amenity:
        for key in dict_amenity.values():
            all_amenity.append(key.to_dict())
    return jsonify(all_amenity)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_amenity(amenity_id):
    """ retrieve a city object """
    amenity_object = {}
    amenity_object = storage.get(classes['Amenity'], amenity_id)
    if not amenity_object:
        abort(404)
    if amenity_object:
        return jsonify(amenity_object.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleting_amenity_object(amenity_id):
    """ deleting an amenity object based on its id """
    amenity_object = {}
    amenity_object = storage.get(classes['Amenity'], amenity_id)
    if not amenity_object:
        abort(404)
    if amenity_object:
        storage.delete(amenity_object)
        storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def new_new_object():
    """ posting of a new amenity """
    amenity_object = request.get_json()
    if not request.get_json():
        abort(400, description='Not JSON')
    if 'name' not in amenity_object:
        abort(400, description='Missing name')
    amenity_instance = classes['Amenity'](**amenity_object)
    storage.new(amenity_instance)
    storage.save()
    return jsonify(amenity_instance.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity_object(amenity_id):
    """ updating existing amenity object """
    amenity_object = request.get_json()
    existing_object = {}
    existing_object = storage.get(classes['Amenity'], amenity_id)
    if not existing_object:
        abort(400)
    if not request.get_json():
        abort(400, description='Not a JSON')
    ignore_list = ['id', 'created_at', 'updated_at']
    for keys, values in amenity_object.items():
        if keys not in ignore_list:
            setattr(existing_object, keys, values)
    storage.save()
    return make_response(jsonify(existing_object.to_dict()), 200)
