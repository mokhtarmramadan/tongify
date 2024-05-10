#!/usr/bin/python3
''' Views packgae '''
from flask import Blueprint

app_view = Blueprint('app_view', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views.user import *
from api.v1.views.posts import *
from api.v1.views.user_urls import *