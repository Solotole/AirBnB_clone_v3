#!/usr/bin/python3
""" view for Review object that handles all default RESTFul API actions """
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


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def retrieve_place_reviews(place_id):
    """ retrieve all review objects of a place connection """
    dictionary = {}
    dictionary = storage.get(classes['Place'], place_id)
    all_list = []
    if dictionary:
        for key in dictionary.reviews:
            if key.place_id == place_id:
                all_list.append(key.to_dict())
    elif not dictionary:
        abort(404)
    return jsonify(all_list)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def retrive_reviews(review_id):
    """ retrieving review objects according to review_id """
    review_object = storage.get(classes['Review'], review_id)
    if not review_object:
        abort(404)
    if review_object:
        return jsonify(review_object.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def deleting_review(review_id):
    """ method to delete review objects according to review_id """
    review_object = storage.get(classes['Review'], review_id)
    if not review_object:
        abort(404)
    elif review_object:
        storage.delete(review_object)
        storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def posting_place(place_id):
    """ posting place object """
    dict_object = request.get_json()
    if request.get_json() is None:
        abort(400, description='Not a JSON')
    place = storage.get(classes['Place'], place_id)
    if not place:
        abort(404)
    if 'text' not in dict_object:
        abort(400, description='Missing text')
    if 'user_id' not in dict_object:
        abort(400, description='Missing user_id')
    user = storage.get(classes['User'], dict_object['user_id'])
    if not user:
        abort(404)
    instance_review = classes['Review'](**dict_object)
    instance_review['place_id'] = place_id
    instance_review.save()
    return jsonify(instance_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def put_method(review_id):
    """ put review object into the database """
    dict_object = request.get_json()
    review_object = storage.get(classes['Review'], review_id)
    if not review_object:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    ignore_list = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for k, val in dict_object.items():
        if k not in ignore_list:
            setattr(review_object, k, val)
    storage.save()
    return jsonify(review_object.to_dict()), 200
