from flask import Blueprint

Assessment = Blueprint('Assessment', __name__)

from . import route
