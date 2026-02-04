from flask import Blueprint

ProctorService = Blueprint('ProctorService', __name__)

from . import route
