#!/usr/bin/env python
# encoding: utf-8


from functools import wraps
from flask import abort
from flask.ext.login import current_user
from .models import User


def administrator_required(func):
    '''judge user is administrator or no'''
    @wraps(func)
    def wrapper(*args, **kw):
        if User.query.filter_by(email=current_user.email).first().permissions == 1:
            abort(403)
        return func(*args, **kw)
    return wrapper
