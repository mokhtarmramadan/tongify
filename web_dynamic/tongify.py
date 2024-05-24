#!/usr/bin/python3
""" Starts a Flash Web Application """
import datetime
from functools import wraps
from flask import Flask, render_template, session, abort, redirect, request, jsonify
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import json
from models import storage
from models.user import User
from models.post import Post
import os
from os import environ
import pathlib
from pip._vendor import cachecontrol
import requests
import uuid


app = Flask(__name__)
app.secret_key = 'tongifybaSNMKrw_69EG?d'


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
GOOGLE_CLIENT_ID = '968902510628-ebukr2p3fa8olcij13mpalotarrsa0in.apps.googleusercontent.com'
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "google.json") 

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    ''' A decorator added to routes to ensure credential presence '''
    @wraps(function)
    def wrapper(*args, **kwargs):
        ''' Returns 401 unauthorized if not login '''
        if "google_id" not in session:
            return redirect('/login')
        else:
            return function()
    return wrapper


@app.route("/login")
def login():
    ''' Opens authorization menue to authorize user '''
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    ''' fetchs token and credentials and POSTS them to the create user API '''
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    if id_info.get("email_verified"):
        ''' If google authenticates the email '''
        user = storage.user_id_by_email(id_info.get('email'))
        user_data = {
            "username": id_info.get("name"),
            "email": id_info.get("email"),
            "image": id_info.get("picture")
        }
        if user is None:
            ''' User has not registered his email to our database "create a new user" '''
            user_url = 'http://0.0.0.0:5050/api/v1/users'
            response = requests.post(user_url, json=user_data)
            if response.status_code == 201:
                data = response.json()
                session["google_id"] = id_info.get("sub")
                session["user_id"] = data['id']
                session['username'] = data['username']
                session['created_at'] = data['created_at']
                session['image'] = data['image']
    
        else:
            ''' User has his email registered already "update user info " '''
            del user_data['email']
            user_id = user.id
            user_url = f'http://0.0.0.0:5050/api/v1/users/{user_id}'
            response = requests.put(user_url, json=user_data)
            if response.status_code == 200:
                session["google_id"] = id_info.get("sub")
                session['user_id'] = user_id
                session['username'] = user.username
                session['created_at'] = user.created_at
                session['image'] = user.image

    return redirect('/profile')


@app.route("/logout")
def logout():
    ''' Clears current session '''
    session.clear()
    return redirect("/")


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/', strict_slashes=False)
def index():
    """ Tongify rooms API """
    return render_template("index.html")

@app.route('/posts', strict_slashes=False)
@login_is_required
def posts():
    """ Tongify posts API """
    posts = storage.all("Post").values()
    this_user = storage.get("User", session['user_id'])
    profile_picture = this_user.image
    return render_template('posts.html', session=session, title="Posts", posts=posts, cash_id=uuid.uuid4())


@app.route('/random', strict_slashes=False)
@login_is_required
def random():
    """ Tongify random-call route """
    this_user = storage.get("User", session['user_id'])
    profile_picture = this_user.image
    return render_template('random.html',  title="Random",profile_picture=profile_picture, cash_id=uuid.uuid4())


@app.route('/profile', strict_slashes=False)
@login_is_required
def profile():
    user = storage.get('User', session['user_id'])
    return render_template('profile.html',  bio=user.bio, title="Profile",session=session, cash_id=uuid.uuid4())

def get_username(user_id):
    " gets username by user_id "
    user = storage.get("User", user_id)
    if user is not None:
        return user.username
    return "Unkown"


def format_time(post_id):
    " Format time "
    from datetime import date, time, datetime
    today_date = str(date.today())
    today_time = str(datetime.now().time())

    post = storage.get("Post", post_id)
    post_date = str(post.created_at.date())
    post_time = str(post.created_at.time())

    if post_date == today_date:
        ''' Posted today '''
        today_hour, today_min, today_sec = today_time.split(":")
        post_hour, post_min, post_sec = post_time.split(":")

        if post_hour == today_hour:
            ''' Posted this hour '''
            if post_min == today_min:
                ''' Posted this minute'''
                return "Now."
            else:
                mins_ago = abs(int(post_min) - int(today_min))
                if mins_ago == 1:
                    return f'A minute ago.'
                else:
                    return f'{mins_ago} minutes ago.'
        else:
            hours_ago = abs(int(post_hour) - int(today_hour))
            if hours_ago == 1:
                return 'An hour ago.'
            else:
                return f'{hours_ago} hours ago.'
    else:
        post_year, post_month, post_day = post_date.split('-')
        today_year, today_month, today_day = today_date.split('-')
        if post_year == today_year:
            ''' Posted this year '''
            if post_month == today_month:
                ''' Posted this month '''
                days_ago = abs(int(post_day) - int(today_day))
                if days_ago == 1:
                    return 'A day ago.'
                else:
                    return f'{days_ago} days ago.'
            else:
                months_ago = abs(int(post_month) - int(today_month))
                if months_ago == 1:
                    return 'A month ago.'
                else:
                    return f'{months_ago} months ago.'
        else:
            years_ago = abs(int(post_year) - int(today_year))
            if years_ago == 1:
                return 'A year ago.'
            else:
                return f'{years_ago} years ago.'


def get_image(user_id):
    " gets user image by user_id "
    user = storage.get("User", user_id)
    if user is not None:
        return user.image
    return "Unkown"

# Make functions global so that all templates can access them
app.add_template_global(get_username, 'get_username')
app.add_template_global(format_time, "format_time")
app.add_template_global(get_image, "get_image")


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)