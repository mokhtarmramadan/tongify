#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from models.user import User
from models.post import Post
from os import environ
from flask import Flask, render_template
import uuid
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/', strict_slashes=False)
def tongify():
    """ tongify API """
    posts = storage.all("Post").values()
    return render_template('posts.html', posts=posts, cash_id=uuid.uuid4())

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

# Make functions global so that all templates can access them
app.add_template_global(get_username, 'get_username')
app.add_template_global(format_time, "format_time")

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)