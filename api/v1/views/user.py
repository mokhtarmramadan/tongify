#!/usr/bin/python3
''' User views '''
from api.v1.views import app_view
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_view.route('/users', methods=['GET'], strict_slashes=False)
@app_view.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    ''' Retrieves a user with ID provided otherwise retrieves all users'''
    if user_id is None:
        all_users = []
        users = storage.all("User").values()
        for user in users:
            all_users.append(user.to_dict())
        return jsonify(all_users)
    else:
        user = storage.get('User', user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_dict())


@app_view.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    ''' Delete User by ID '''
    if user_id:
        user = storage.get('User', user_id)
        if user is None:
            abort(404)
        else:
            user = storage.get('User', user_id)
            storage.delete(user)
            storage.save()
            return '{}'
    else:
        abort(404)


@app_view.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """ Creates a User """
    if not request.get_json() or not request.is_json:
        abort(440, 'Not a JSON')
    if request.headers.get('Content-Type') != 'application/json':
        abort(440)
    if 'username' not in request.get_json():
        abort(400, 'Missing name')
    if 'email' not in request.get_json():
        abort(400, "Missing email")
    new_user = User()
    never_set = ['id', 'created_at', 'updated_at', "__class__",
                    "cam", "chat", 'followers', 'following', 'mic', 'vip']

    for k, v in request.json.items():
        if hasattr(new_user, k):
            if k not in never_set:
                if k == 'password':
                    v = hash_password(v)
                setattr(new_user, k, v)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_view.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id=None):
    ''' Update user '''
    if user_id is None:
        abort(404)
    if not request.get_json() or not request.is_json:
        abort(400, 'Not a JSON')
    if request.headers.get('Content-Type') != 'application/json':
        abort(400)
    user = storage.get('User', user_id)
    if user is None:
        abort(404, "User id doesn't exist")
    never_update = ['id', 'created_at', 'updated_at', '__class__']
    for k, v in request.json.items():
        if k not in never_update:
            if hasattr(user, k):
                if k == 'password':
                    v = hash_password(v)
                setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200


def hash_password(plain_password):
    ''' Encrypts plain passwords into their hexadecimal hash'''
    from hashlib import md5
    md5_object = md5()
    
    # Put plain text in byte-literals format
    # and pass it to the object
    plain_password = plain_password.encode('utf-8')
    md5_object.update(plain_password)

    # Hexadecimal representation of plain
    hashed_password = md5_object.hexdigest()
    return hashed_password
