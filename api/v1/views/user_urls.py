#!/usr/bin/python3
''' user_urls view '''
from flask import jsonify, abort, request
from api.v1.views import app_view
from models import storage
from models.user_urls import User_urls


@app_view.route('/users/<user_id>/user_urls', strict_slashes=False, methods=['GET'])
def get_urls(user_id=None):
    ''' Gets all urls of a user or A specific url of a user '''
    if user_id is None:
        abort(404)
    user_urls = []
    all_users_urls = storage.all('User_urls').values()
    for all_users_url in all_users_urls:
        if all_users_url.user_id == user_id:
            user_urls.append(all_users_url.to_dict())
    return jsonify(user_urls)


@app_view.route('/users/<user_id>/user_urls/<url_id>', strict_slashes=False, methods=['DELETE'])
def Delete_url(user_id=None, url_id=None):
    ''' Deletes a url of a specific user '''
    if user_id is None or url_id is None:
        abort(404)
    target_url = storage.get('User_urls', url_id)
    if target_url is None:
        abort(404)
    if target_url.user_id != user_id:
        abort(404)
    storage.delete(target_url)
    storage.save()
    return jsonify({}), 200


@app_view.route('/users/<user_id>/user_urls', strict_slashes=False, methods=['POST'])
def Update_url(user_id=None, url_id=None):
    ''' Creates a url of a specific user '''
    if user_id is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'website_name' not in request.get_json():
        abort(400, "Missing website name")
    if 'url' not in request.get_json():
        abort(400, "Missing URL")
    if storage.get('User', user_id) is None:
        abort(400, "User doesn't exist")
    never_set = ['id', 'created_at', 'updated_at', "__class__", 'user_id']
    new_url = User_urls()
    new_url.user_id = user_id
    for k, v in request.json.items():
        if hasattr(new_url, k):
            if k not in never_set:
                setattr(new_url, k, v)
    storage.new(new_url)
    storage.save()
    return jsonify(new_url.to_dict()), 201



@app_view.route('/users/<user_id>/user_urls/<url_id>', strict_slashes=False, methods=['PUT'])
def Create_url(user_id=None, url_id=None):
    ''' Updates a url of a specific user '''
    if user_id is None or url_id is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
 
    never_update = ['id', 'created_at', 'updated_at', '__class__', 'user_id']
    target_url = storage.get('User_urls', url_id)
    if target_url is None:
        abort(404)
    if target_url.user_id == user_id:
        for k, v in request.json.items():
            if hasattr(target_url, k):
                if k not in never_update:
                    setattr(target_url, k, v)
    storage.save()
    return jsonify(target_url.to_dict()), 200
