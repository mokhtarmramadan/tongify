#!/usr/bin/python3
''' Posts view '''
from flask import jsonify, abort, request
from api.v1.views import app_view
from models import storage
from models.post import Post


@app_view.route('/posts', methods=['GET'], strict_slashes=False)
@app_view.route('users/<user_id>/posts/', methods=['GET'], strict_slashes=False)
def get_post(user_id=None):
    ''' Retrieves a post with ID provided otherwise retrieves all posts'''
    all_posts = []
    posts = storage.all("Post").values()
    if user_id is None:
        ''' Retrieve all posts if no user_id provided '''
        for post in posts:
            all_posts.append(post.to_dict())
    else:
        ''' Retrieve posts for a user by user_id'''
        if user_id is None:
            abort(404)
        for post in posts:
            if post.user_id == user_id:
                all_posts.append(post.to_dict())
    return jsonify(all_posts)


@app_view.route('/users/<user_id>/posts/<post_id>', strict_slashes=False, methods=['DELETE'])
def delete_post(post_id=None, user_id=None):
    ''' Delete Post '''
    if post_id is None or user_id is None:
        abort(404)
    post = storage.get('Post', post_id)
    if post is None:
        abort(404)
    if storage.get('User', user_id) is None:
        abort(404)
    if post.user_id != user_id:
        abort(404)
    storage.delete(post)
    storage.save()
    return jsonify({}), 200


@app_view.route('/users/<user_id>/posts', strict_slashes=False, methods=['POST'])
def create_post(user_id=None):
    """ Creates a post """
    if user_id is None:
        abort(404, "missing user_id")
    if not request.get_json() or not request.is_json:
        abort(400, 'Not a JSON')
    if request.headers.get('Content-Type') != 'application/json':
        abort(400)
    if 'title' not in request.get_json():
        abort(400, 'Missing title')
    if 'content' not in request.get_json():
        abort(400, 'Missing content')
    user = storage.get("User", user_id)
    if user is None:
        abort(400, "User ID does not exist")
    new_post = Post()
    new_post.user_id = user_id
    never_set = ['id', 'created_at', 'updated_at', '__class__', 'user_id']
    for k, v in request.json.items():
        if hasattr(new_post, k):
            if k not in never_set:
                setattr(new_post, k, v)
    storage.new(new_post)
    storage.save()
    return jsonify(new_post.to_dict()), 201


@app_view.route('/users/<user_id>/posts/<post_id>', strict_slashes=False, methods=['PUT'])
def update_post(post_id=None, user_id=None):
    ''' Update post '''
    if post_id is None or user_id is None:
        abort(404)
    if not request.get_json() or not request.is_json:
        abort(400, 'Not a JSON')
    if request.headers.get('Content-Type') != 'application/json':
        abort(400)
    post = storage.get('Post', post_id)
    if post is None:
        abort(404, "Post id doesn't exist")
    if post.user_id != user_id:
        abort(404)
    never_update = ['id', 'created_at', 'updated_at', '__class__', 'user_id']
    for k, v in request.json.items():
        if k not in never_update:
            if hasattr(post, k):
                setattr(post, k, v)
    storage.save()
    return jsonify(post.to_dict()), 200

