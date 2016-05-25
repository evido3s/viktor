#!/usr/bin/env python
# encoding: utf-8


from flask import Blueprint
from .. import celery


service = Blueprint('service', __name__)
celery = celery


from . import views
