#!/usr/bin/python3
''' Returns the status of the request '''
from api.v1.views import app_view
from flask import jsonify 
from models import storage

@app_view.route('/status', strict_slashes=False)
def status():
    status = {
        "status": "OK"
    }
    return jsonify(status)

@app_view.route('/stats', strict_slashes=False)
def stats():
    stats = {
        "User": storage.count("User"),
        "Post": storage.count("Post")
    }
    return jsonify(stats)