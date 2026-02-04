from flask import Blueprint

PlaybackService = Blueprint('PlaybackService', __name__)

from . import route
