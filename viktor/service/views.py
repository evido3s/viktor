#!/usr/bin/env python
# encoding: utf-8


from flask import render_template, request, current_app
from flask.ext.login import login_required, current_user
from . import service
from .config import *
from .. import db
from ..decorators import administrator_required
from ..models import Tasks, Hosts
from .modules.ping import ping
from .modules.update import _update
from datetime import datetime


def search(r):
    return r.ready()


@service.route('/pong', methods=['GET', 'POST'])
@login_required
def Test():
    page = request.args.get('page', 1, type=int)
    pagination = Hosts.query.order_by(Hosts.id.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'],
        error_out=False)
    hosts = pagination.items

    if request.form.get('run', None):
        host = request.form.getlist('run')
        for h in host:
            r = ping.delay('h')
            stat = search(r)
            tasks = Tasks(uuid = str(r),
                          task = 'Ping',
                          time = str(datetime.now()),
                          objective = h,
                          state = stat)
            db.session.add(tasks)
        return render_template('service/result.html')
    return render_template('service/service.html', hosts=hosts, pagination=pagination)


@service.route('/update', methods=['GET', 'POST'])
@login_required
def Update():
    page = request.args.get('page', 1, type=int)
    pagination = Hosts.query.order_by(Hosts.id.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'],
        error_out=False)
    hosts = pagination.items

    if request.form.get('run', None):
        host = request.form.getlist('run')
        for h in host:
            r = _update.delay('h')
            stat = search(r)
            tasks = Tasks(uuid = str(r),
                          task = 'Update',
                          time = str(datetime.now()),
                          objective = h,
                          state = stat)
            db.session.add(tasks)
        return render_template('service/result.html')
    return render_template('service/service.html', hosts=hosts, pagination=pagination)
