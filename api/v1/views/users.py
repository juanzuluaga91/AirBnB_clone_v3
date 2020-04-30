#!/usr/bin/python3
"""users view"""

from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """get user information for all users"""
    dict_users = []
    all_users = storage.all("User").values()
    for user in all_users:
        dict_users.append(user.to_dict())
    return jsonify(dict_users)


@app_views.route('/users/<id>', methods=['GET'],
                 strict_slashes=False)
def user_by_id(id):
    """retrieves the user by the given id """
    dict_users = storage.all(User)
    key = "User." + id
    obj = None
    if key in dict_users:
        obj = dict_users[key].to_dict()
    if obj is None:
        abort(404)
    obj = jsonify(obj)
    return (obj)


@app_views.route('/users/<id>', methods=['DELETE'], strict_slashes=False)
def delete_user_id(id):
    """delete user by id"""
    dict_users = storage.all(User)
    key = "User." + id
    if key in dict_users:
        obj = dict_users[key]
        obj.delete()
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """get request and post new user"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    new_user = request.get_json()
    if 'email' not in new_user:
        return abort(400, description="Missing email")
    if 'password' not in new_user:
        return abort(400, description="Missing password")
    obj_user = User()
    obj_user.email = new_user['email']
    obj_user.password = new_user['password']
    storage.save()
    dict_obj = obj_user.to_dict()
    return make_response(jsonify(dict_obj), 201)


@app_views.route('/users/<id>', methods=['PUT'], strict_slashes=False)
def edit_usr_id(id):
    """edit user by id"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    dict_users = storage.all(User)
    new_user = request.get_json()
    u_key = "User." + id
    if u_key in dict_users:
        obj = dict_users[u_key]
        for key, value in new_user.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(obj, key, value)
        obj.save()
        return jsonify(obj.to_dict())
    else:
        abort(404)
