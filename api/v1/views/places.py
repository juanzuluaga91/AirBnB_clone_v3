#!/usr/bin/python3
"""view for Cities objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from json import dumps
from flask import abort, request, jsonify, make_response


@app_views.route('/cities/<id>/places',
                 methods=['GET'], strict_slashes=False)
def places_by_city(id):
    """Retrieves the list of all Places objects of a City"""
    obj_list = []
    all_cities = storage.all(City)
    key = "City." + id
    if key in all_cities:
        places_list = all_cities[key].places
    else:
        abort(404)
    for place in places_list:
        obj = place.to_dict()
        obj_list.append(obj)
    obj_list = jsonify(obj_list)
    return (obj_list)


@app_views.route('/places/<id>',
                 methods=['GET'], strict_slashes=False)
def places_by_id(id):
    """Retrieves the list of City by id"""
    obj = None
    all_places = storage.all(Place)
    key = "Place." + id
    if key in all_places:
        obj = all_places[key].to_dict()
    if obj is None:
        abort(404)
    obj = jsonify(obj)
    return (obj)


@app_views.route('/places/<id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_by_id(id):
    """delete a place by id"""
    dict_places = storage.all(Place)
    key = "Place." + id
    if key in dict_places:
        obj = dict_places[key]
        obj.delete()
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """get request and post new Place"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    new_place = request.get_json()
    all_cities = storage.all(City)
    if 'name' not in new_place:
        return abort(400, description="Missing name")
    if 'user_id' not in new_place:
        return abort(400, description="Missing user_id")
    key = "City." + city_id
    atributes = ['number_rooms', 'number_bathrooms',
                 'max_guest', 'price_by_night', 'latitude',
                 'longitude', 'description']
    if key in all_cities:
        obj_city = all_cities[key]
        obj_places = Place()
        obj_places.city_id = obj_city.id
        obj_places.user_id = new_place["user_id"]
        obj_places.name = new_place["name"]
        for p_key, p_val in new_place.items():
            if p_key in atributes:
                setattr(obj_places, p_key, p_val)
        obj_places.save()
        obj_places = obj_places.to_dict()
        return make_response(jsonify(obj_places), 201)
    else:
        abort(404)
