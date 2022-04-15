import re, requests, random, time
from flask import Blueprint, render_template, request, flash, jsonify
from flask.helpers import url_for
from flask_sqlalchemy.model import should_set_tablename
from . import db
from .db_models import User, Img, Stream
from flask_login import login_required, current_user
from werkzeug.utils import redirect, secure_filename
from werkzeug.security import generate_password_hash
import base64, compress_pickle, pandas as pd, numpy as np, os, shutil
from opentok import Client
from dotenv import load_dotenv

## init env variables
load_dotenv()

## init main app server
main = Blueprint('main', __name__)

## init opentok API
api_key = os.getenv('OPEN_TOK_KEY')
opentok = Client(api_key, os.getenv('OPEN_TOK_SECRET'))

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/news")
def news():
    return render_template("news.html")

@main.route("/contact")
def contact():
    return render_template("contact.html")

@main.route("/feed")
def feed():
    return render_template("feed.html")

@main.route("/monetize")
def monetize():
    return render_template("monetize.html")

@main.route("/create_stream")
def create_stream():
    session = opentok.create_session()
    token = opentok.generate_token(session.session_id)

    return render_template("stream.html", api_key=api_key, session_id=session.session_id, token=token)