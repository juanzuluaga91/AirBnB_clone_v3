#!/usr/bin/python3
"""view for State objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from models import storage
from models.state import State
from json import dumps
from api.v1.app import *
from flask import abort, request, jsonify, make_response


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all State"""
    dict_states = storage.all(State)
    object_list = []
    for value in dict_states.values():
        obj = value.to_dict()
        object_list.append(obj)
    object_list = jsonify(object_list)
    return (object_list)


@app_views.route('/states/<id>', methods=['GET'], strict_slashes=False)
def states_by_id(id):
    """retrieves the state by the given id """
    dict_states = storage.all(State)
    key = "State." + id
    obj = None
    if key in dict_states:
        obj = dict_states[key].to_dict()
    if obj is None:
        abort(404)
    obj = jsonify(obj)
    return (obj)


@app_views.route('/states/<id>', methods=['DELETE'], strict_slashes=False)
def delete_by_id(id):
    """delete state by id"""
    dict_states = storage.all(State)
    key = "State." + id
    if key in dict_states:
        obj = dict_states[key]
        obj.delete()
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """get request and post new state"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    new_state = request.get_json()
    if 'name' in new_state:
        obj_state = State()
        obj_state.name = new_state['name']
        storage.new(obj_state)
        storage.save()
        dict_obj = obj_state.to_dict()
        return make_response(jsonify(dict_obj), 201)
    else:
        abort(400, description="Missing name")


@app_views.route('/states/<id>', methods=['PUT'], strict_slashes=False)
def edit_by_id(id):
    """edit state by id"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    dict_states = storage.all(State)
    new_state = request.get_json()
    key = "State." + id
    if key in dict_states:
        if "name" in new_state:
            obj = dict_states[key]
            obj.name = new_state["name"]
            storage.save()
            obj = obj.to_dict()
            return make_response(jsonify(obj), 200)
        else:
            abort(404)
    else:
        abort(404)
