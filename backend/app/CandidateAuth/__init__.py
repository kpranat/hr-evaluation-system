from flask import Blueprint

CandidateAuth = Blueprint("CandidateAuth", __name__,url_prefix= " ")

from . import route