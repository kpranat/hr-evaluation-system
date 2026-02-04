from flask import Blueprint

psychometric_bp = Blueprint('psychometric', __name__)

from . import route
