#!/usr/bin/python3
"""Amenities view"""

from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """get information from all amenities"""
    dict_amenities = []
    all_amenities = storage.all("Amenity").values()
    for am in all_amenities:
        dict_amenities.append(am.to_dict())
    return jsonify(dict_amenities)


@app_views.route('/amenities/<id>', methods=['GET'],
                 strict_slashes=False)
def amenities_by_id(id):
    """retrieves the amenities by the given id """
    dict_amenities = storage.all(Amenity)
    key = "Amenity." + id
    obj = None
    if key in dict_amenities:
        obj = dict_amenities[key].to_dict()
    if obj is None:
        abort(404)
    obj = jsonify(obj)
    return (obj)


@app_views.route('/amenities/<id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity_id(id):
    """delete amenity by id"""
    dict_amenities = storage.all(Amenity)
    key = "Amenity." + id
    if key in dict_amenities:
        obj = dict_amenities[key]
        obj.delete()
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """get request and post new amenity"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    new_amenity = request.get_json()
    if 'name' not in new_amenity:
        return abort(400, description="Missing name")
    obj_amenity = Amenity()
    obj_amenity.name = new_amenity['name']
    storage.new(obj_amenity)
    storage.save()
    dict_obj = obj_amenity.to_dict()
    return make_response(jsonify(dict_obj), 201)


@app_views.route('/amenities/<id>', methods=['PUT'], strict_slashes=False)
def edit_amnty_id(id):
    """edit Amenity by id"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    dict_amenities = storage.all(Amenity)
    new_amenity = request.get_json()
    a_key = "Amenity." + id
    if a_key in dict_amenities:
        obj = dict_amenities[a_key]
        for key, value in new_amenity.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(obj, key, value)
        obj.save()
        return jsonify(obj.to_dict())
    else:
        abort(404)
