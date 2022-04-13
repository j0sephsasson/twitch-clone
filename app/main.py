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
opentok = Client(os.getenv('OPEN_TOK_KEY'), os.getenv('OPEN_TOK_SECRET'))

# session = opentok.create_session()
@main.route("/")
def index():
    # session_id = session.session_id
    # token = opentok.generate_token(session_id)

    return render_template("index.html")