#!/usr/bin/python3
""" module defining routes for amenity class """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
classes = {"User": User}


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def getting_all_user_objects():
    """ getting a list of all objects """
    dict_user = {}
    dict_user = storage.all(classes['User'])
    all_user = []
    if dict_user:
        for user in dict_user.values():
            all_user.append(user.to_dict())
    return jsonify(all_user)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def retrieve_users(user_id):
    """ retrieve a user object """
    user_object = {}
    user_object = storage.get(classes['User'], user_id)
    if not user_object:
        abort(404)
    if user_object:
        return jsonify(user_object.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def deleting_user_object(user_id):
    """ deleting an user object based on its id """
    user_object = {}
    user_object = storage.get(classes['User'], user_id)
    if not user_object:
        abort(404)
    if user_object:
        storage.delete(user_object)
        storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def posting_user_object():
    """ posting of a new user data """
    user_object = request.get_json()
    if not request.get_json():
        abort(400, description='Not JSON')
    if 'email' not in user_object:
        abort(400, description='Misiing email')
    if 'password' not in user_object:
        abort(400, description='Misiing password')
    user_instance = classes['User'](**user_object)
    user_instance.save()
    return jsonify(user_instance.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def putting_user_object(user_id):
    """ updating existing user object """
    user_object = request.get_json()
    existing_object = {}
    existing_object = storage.get(classes['User'], user_id)
    if not existing_object:
        abort(400)
    if not request.get_json():
        abort(400, description='Not a JSON')
    ignore_list = ['id', 'email', 'created_at', 'updated_at']
    for keys, values in user_object.items():
        if keys not in ignore_list:
            setattr(existing_object, keys, values)
    storage.save()
    return jsonify(existing_object.to_dict()), 200
