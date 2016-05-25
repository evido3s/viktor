#!/usr/bin/env python
# encoding: utf-8


from flask import render_template, request, current_app
from flask.ext.login import login_required, current_user
from . import service
from .config import *
from .. import db
from ..decorators import administrator_required
from ..models import User, Hosts
from .modules.ping import ping
from datetime import datetime


def search(r):
    return r.ready()


@service.route('/pong', methods=['GET', 'POST'])
@login_required
def service():
    page = request.args.get('page', 1, type=int)
    pagination = Hosts.query.order_by(Hosts.id.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'],
        error_out=False)
    hosts = pagination.items

    task = {}
    task[current_user] = {}

    if request.form.get('run', None):
        host = request.form.getlist('run')
        for h in host:
            r = ping.delay('h')
            task[current_user]['time'] = str(datetime.now())
            task[current_user]['uuid'] = str(r)
            task[current_user]['task'] = 'ping'
            task[current_user]['objective'] = h
        task[current_user]['state'] = search(r)
        print task
        return render_template('service/result.html')
    return render_template('service/service.html', hosts=hosts, pagination=pagination)
