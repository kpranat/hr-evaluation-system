"""
TextBased Blueprint
Handles text-based question and answer management
"""
from flask import Blueprint

TextBased = Blueprint('TextBased', __name__)

from . import route
