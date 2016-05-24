#!/usr/bin/env python
# encoding: utf-8


from flask import render_template
from . import main


@main.app_errorhandler(403)
def forbidden(e):
    '''403 error page'''
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    '''404 error page'''
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    '''500 error page'''
    return render_template('500.html'), 500
