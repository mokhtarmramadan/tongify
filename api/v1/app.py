#!/usr/bin/python3
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_view
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_view)


@app.teardown_appcontext
def teardown(exception):
    ''' Handles teardown '''
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ handler for 404 errors """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, threaded=True, debug=True)
