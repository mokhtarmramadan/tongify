#!/usr/bin/python3
''' Posts view '''
from flask import jsonify, abort, request
from api.v1.views import app_view
from models import storage
from models.post import Post


@app_view.route('/posts', methods=['GET'], strict_slashes=False)
@app_view.route('/posts/<post_id>', methods=['GET'], strict_slashes=False)
def get_post(post_id=None):
    ''' Retrieves a post with ID provided otherwise retrieves all posts'''
    if post_id is None:
        all_posts = []
        posts = storage.all("Post").values()
        if request.is_json:
            if "user_id" in request.get_json():
                # To retrive all posts of a specific user id
                user = storage.get("User", request.json['user_id'])
                if user is None:
                    abort(400, "User does not exist")
                for post in posts:
                    post = post.to_dict()
                    if post['user_id'] == request.json["user_id"]:
                        all_posts.append(post)
        else:
            # Retrieve all posts otherwise
            for post in posts:
                all_posts.append(post.to_dict())
        return jsonify(all_posts)
    else:
        # Retrieve a specific post by post id
        post = storage.get('Post', post_id)
        if post is None:
            abort(404)
        return jsonify(post.to_dict())


@app_view.route('/posts/<post_id>', strict_slashes=False, methods=['DELETE'])
def delete_post(post_id):
    ''' Delete Post by ID '''
    if post_id:
        post = storage.get('Post', post_id)
        if post is None:
            abort(404)
        else:
            post = storage.get('Post', post_id)
            storage.delete(post)
            storage.save()
            return '{}'
    else:
        abort(404)


@app_view.route('/posts', strict_slashes=False, methods=['POST'])
def create_post():
    """ Creates a post """
    if not request.get_json() or not request.is_json:
        abort(400, 'Not a JSON')
    if request.headers.get('Content-Type') != 'application/json':
        abort(400)
    if 'title' not in request.get_json():
        abort(400, 'Missing title')
    if 'content' not in request.get_json():
        abort(400, 'Missing content')
    if 'user_id' not in request.get_json():
        abort(400, "Missing user_id")
    user = storage.get("User", request.json['user_id'])
    if user is None:
        abort(400, "User ID does not exist")
    new_post = Post()
    never_set = ['id', 'created_at', 'updated_at', '__class__']
    for k, v in request.json.items():
        if hasattr(new_post, k):
            if k not in never_set:
                setattr(new_post, k, v)
    storage.new(new_post)
    storage.save()
    return jsonify(new_post.to_dict()), 201


@app_view.route('/posts/<post_id>', strict_slashes=False, methods=['PUT'])
def update_post(post_id=None):
    ''' Update post '''
    if post_id is None:
        abort(404)
    if not request.get_json() or not request.is_json:
        abort(400, 'Not a JSON')
    if request.headers.get('Content-Type') != 'application/json':
        abort(400)
    post = storage.get('Post', post_id)
    if post is None:
        abort(404, "Post id doesn't exist")
    never_update = ['id', 'created_at', 'updated_at', '__class__']
    for k, v in request.json.items():
        if k not in never_update:
            if hasattr(post, k):
                setattr(post, k, v)
    storage.save()
    return jsonify(post.to_dict()), 200

