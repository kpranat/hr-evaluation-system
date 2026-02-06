from flask import Blueprint

CandidateAuth = Blueprint("CandidateAuth", __name__)

from . import route