from flask import Blueprint

RecruiterAuth = Blueprint('RecruiterAuth', __name__)

from . import route
