#!/usr/bin/env python
# encoding: utf-8


import os
from flask import render_template, request, current_app, redirect, flash
from flask.ext.login import login_required, current_user
from . import service
from .config import *
from .. import db
from ..decorators import administrator_required
from ..models import Tasks, Hosts
from .modules.ping import ping
from .modules.update import _update
from .modules.java import _java
from datetime import datetime


search = lambda r: r.ready()


@service.route('/service', methods=['GET', 'POST'])
@login_required
def se():
    return render_template('service/service.html')


@service.route('/update', methods=['GET', 'POST'])
@login_required
def Update():
    page = request.args.get('page', 1, type=int)
    pagination = Hosts.query.order_by(Hosts.id.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'],
        error_out=False)
    hosts = pagination.items

    auth = request.form.get('passwd', '')
    if auth == '':
        key_pwd = os.path.join(BASEPATH, '.key')
        key_file = os.path.join(key_pwd, '%s' % str(current_user))
        if current_user.pri_key is None:
            flash(u'没有使用中的密码或者私钥')
            return render_template('service/update.html', hosts=hosts, pagination=pagination)
        else:
            with open(key_file, 'w') as f:
                f.write(current_user.pri_key)
            if request.form.get('run', None):
                host = request.form.getlist('run')
                for h in host:
                    r = _update.delay(h, passwd=None, key_filename=key_file)
                    stat = search(r)
                    tasks = Tasks(uuid = str(r),
                                  user = str(current_user),
                                  task = u'初始化',
                                  time = str(datetime.now()),
                                  objective = h,
                                  state = stat)
                    db.session.add(tasks)
                return render_template('service/result.html')
    else:
        if request.form.get('run', None):
            host = request.form.getlist('run')
            for h in host:
                r = _update.delay(h, passwd=auth)
                stat = search(r)
                tasks = Tasks(uuid = str(r),
                              user = str(current_user),
                              task = u'初始化',
                              time = str(datetime.now()),
                              objective = h,
                              state = stat)
                db.session.add(tasks)
            return render_template('service/result.html')


    os.remove(key_file)
    return render_template('service/update.html', hosts=hosts, pagination=pagination)


@service.route('/initjava', methods=['GET', 'POST'])
@login_required
def Java():
    page = request.args.get('page', 1, type=int)
    pagination = Hosts.query.order_by(Hosts.id.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'],
        error_out=False)
    hosts = pagination.items

    auth = request.form.get('passwd', '')
    uri = request.form.get('uri', '')

    if uri == '':
        flash(u'没有下载链接啊')
        return render_template('service/java.html', hosts=hosts, pagination=pagination)

    if auth == '':
        key_pwd = os.path.join(BASEPATH, '.key')
        key_file = os.path.join(key_pwd, '%s' % str(current_user))
        if current_user.pri_key is None:
            flash(u'没有使用中的密码或者私钥')
            return render_template('service/java.html', hosts=hosts, pagination=pagination)
        else:
            with open(key_file, 'w') as f:
                f.write(current_user.pri_key)
            if request.form.get('run', None):
                host = request.form.getlist('run')
                for h in host:
                    print uri
                    r = _java.delay(h, uri, passwd=None, key_filename=key_file)
                    stat = search(r)
                    tasks = Tasks(uuid = str(r),
                                  user = str(current_user),
                                  task = u'初始化',
                                  time = str(datetime.now()),
                                  objective = h,
                                  state = stat)
                    db.session.add(tasks)
                return render_template('service/result.html')
    else:
        if request.form.get('run', None):
            host = request.form.getlist('run')
            for h in host:
                r = _java.delay(h, uri, passwd=auth)
                stat = search(r)
                tasks = Tasks(uuid = str(r),
                              user = str(current_user),
                              task = u'初始化',
                              time = str(datetime.now()),
                              objective = h,
                              state = stat)
                db.session.add(tasks)
            return render_template('service/result.html')


    os.remove(key_file)
    return render_template('service/java.html', hosts=hosts, pagination=pagination)


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
                          user = str(current_user),
                          task = 'Ping',
                          time = str(datetime.now()),
                          objective = h,
                          state = stat)
            db.session.add(tasks)
        return render_template('service/result.html')
    return render_template('service/service.html', hosts=hosts, pagination=pagination)
