#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage as s
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def define_state():
    """
    return the list of states
    """
    state_list = []
    state_obj = s.all(State)
    for obj in state_obj.values():
        state_list.append(obj.to_dict())
    return jsonify(state_list)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def creat_state():
    """
    create state route
    :return: newly created state obj
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, description='Not a JSON')
    if "name" not in state_json:
        abort(400, description='Missing name')
    new_state = State(**state_json)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    gets a specific State object by ID
    :param state_id: state object id
    :return: state obj with the specified id or error
    """
    fetched_obj = s.get(State, state_id)
    if not fetched_obj:
        abort(404)
    return jsonify(fetched_obj.to_dict())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    updates specific State object by ID
    """
    state_json = request.get_json(silent=True)
    if not request.get_json():
        abort(400, description='Not a JSON')
    fetched_obj = s.get(State, state_id)
    if not fetched_obj:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return make_response(jsonify(fetched_obj.to_dict()), 200)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete(state_id):
    """
    deletes State by id
    """
    fetched_obj = s.get(State, state_id)
    if not fetched_obj:
        abort(404)
    s.delete(fetched_obj)
    s.save()
    return make_response(jsonify({}), 200)
