#!/usr/bin/python3
"""view for Cities objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from models import storage
from models.state import State, City
from json import dumps
from api.v1.app import *
from flask import abort, request, jsonify, make_response


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities_by_state(state_id):
    """Retrieves the list of all City objects of a State"""
    obj_list = []
    all_state = storage.all(State)
    key = "State." + state_id
    if key in all_state:
        cities_list = all_state[key].cities
    else:
        abort(404)
    for city in cities_list:
        obj = city.to_dict()
        obj_list.append(obj)
    obj_list = jsonify(obj_list)
    return (obj_list)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def cities_by_id(city_id):
    """Retrieves the list of City by id"""
    obj = None
    all_cities = storage.all(City)
    key = "City." + city_id
    if key in all_cities:
        obj = all_cities[key].to_dict()
    if obj is None:
        abort(404)
    obj = jsonify(obj)
    return (obj)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city_by_id(city_id):
    """delete city by id"""
    dict_cities = storage.all(City)
    key = "City." + city_id
    if key in dict_cities:
        obj = dict_cities[key]
        obj.delete()
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """get request and post new City"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    new_city = request.get_json()
    all_states = storage.all(State)
    key = "State." + state_id
    if key in all_states:
        obj_state = all_states[key]
        if "name" in new_city:
            obj_city = City()
            obj_city.name = new_city["name"]
            obj_city.state_id = obj_state.id
            obj_city.save()
            obj_city = obj_city.to_dict()
            return make_response(jsonify(obj_city), 201)
        else:
            abort(400, description="Missing name")
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def edit_city_by_id(city_id):
    """edit city by id"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    dict_cities = storage.all(City)
    key = "City." + city_id
    new_city = request.get_json()
    if key in dict_cities:
        if "name" in new_city:
            obj_city = dict_cities[key]
            obj_city.name = new_city["name"]
            storage.save()
            obj_city = obj_city.to_dict()
            return make_response(jsonify(obj_city), 200)
        else:
            abort(404)
    else:
        abort(404)
