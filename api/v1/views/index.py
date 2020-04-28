#!/usr/bin/python3
""" view for status of the api"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
from json import dumps
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns a JSON: "status": "OK"""
    status_dict = {"status": "OK"}
    return jsonify(status_dict)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """returns a JSON: "status": "OK"""
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    dict_count = {}
    i = 0
    for key, value in classes.items():
        count = storage.count(value)
        dict_count[key] = count
    dict_count = jsonify(dict_count)
    return (dict_count)
