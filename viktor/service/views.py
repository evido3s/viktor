#!/usr/bin/env python
# encoding: utf-8


import os
from flask import render_template, request, current_app, redirect, url_for
from flask.ext.login import login_required, current_user
from werkzeug import secure_filename
from . import service
from .config import *
from .. import db
from ..decorators import administrator_required
from ..models import Tasks, Hosts
from .modules.ping import ping
from .modules.update import _update
from .modules.java import _java
from .modules.node import _node
from .modules.nginx import _nginx
from .modules.redis import _redis
from .modules.rabbitmq import _rabbitmq
from datetime import datetime


search = lambda r: r.ready()


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in current_app.config['ALLOWEN_EXTENSIONS']


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
            return redirect('service/update.html', hosts=hosts, pagination=pagination)
        else:
            with open(key_file, 'w') as f:
                f.write(current_user.pri_key)
            if request.form.get('run', None):
                host = request.form.getlist('run')
                for h in host:
                    r = _update.delay(h, passwd=None, key_filename=key_file)
                    stat = search(r)
                    tasks = Tasks(uuid = str(r),
                                  tasktouser = current_user.realname,
                                  task = 'UPDATE',
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
                              tasktouser = current_user.realname,
                              task = 'UPDATE',
                              time = str(datetime.now()),
                              objective = h,
                              state = stat)
                db.session.add(tasks)
            return render_template('service/result.html')


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
        return render_template('service/java.html', hosts=hosts, pagination=pagination)

    if auth == '':
        key_pwd = os.path.join(BASEPATH, '.key')
        key_file = os.path.join(key_pwd, '%s' % str(current_user))
        if current_user.pri_key is None:
            return render_template('service/java.html', hosts=hosts, pagination=pagination)
        else:
            with open(key_file, 'w') as f:
                f.write(current_user.pri_key)
            if request.form.get('run', None):
                host = request.form.getlist('run')
                for h in host:
                    r = _java.delay(h, uri, passwd=None, key_filename=key_file)
                    stat = search(r)
                    tasks = Tasks(uuid = str(r),
                                  tasktouser = current_user.realname,
                                  task = 'JAVA',
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
                              tasktouser = current_user.realname,
                              task = 'JAVA',
                              time = str(datetime.now()),
                              objective = h,
                              state = stat)
                db.session.add(tasks)
            return render_template('service/result.html')

    return render_template('service/java.html', hosts=hosts, pagination=pagination)


@service.route('/initnode', methods=['GET', 'POST'])
@login_required
def Node():
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
            return render_template('service/node.html', hosts=hosts, pagination=pagination)
        else:
            with open(key_file, 'w') as f:
                f.write(current_user.pri_key)
            if request.form.get('run', None):
                host = request.form.getlist('run')
                for h in host:
                    r = _node.delay(h, passwd=None, key_filename=key_file)
                    stat = search(r)
                    tasks = Tasks(uuid = str(r),
                                  tasktouser = current_user.realname,
                                  task = 'Node',
                                  time = str(datetime.now()),
                                  objective = h,
                                  state = stat)
                    db.session.add(tasks)
                return render_template('service/result.html')
    else:
        if request.form.get('run', None):
            host = request.form.getlist('run')
            for h in host:
                r = _node.delay(h, passwd=auth)
                stat = search(r)
                tasks = Tasks(uuid = str(r),
                              tasktouser = current_user.realname,
                              task = 'Node',
                              time = str(datetime.now()),
                              objective = h,
                              state = stat)
                db.session.add(tasks)
            return render_template('service/result.html')

    return render_template('service/node.html', hosts=hosts, pagination=pagination)


@service.route('/initnginx', methods=['GET', 'POST'])
@login_required
def Nginx():
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
            return render_template('service/nginx.html', hosts=hosts, pagination=pagination)
        else:
            with open(key_file, 'w') as f:
                f.write(current_user.pri_key)
            if request.form.get('run', None):
                host = request.form.getlist('run')
                for h in host:
                    r = _nginx.delay(h, passwd=None, key_filename=key_file)
                    stat = search(r)
                    tasks = Tasks(uuid = str(r),
                                  tasktouser = current_user.realname,
                                  task = 'Nginx',
                                  time = str(datetime.now()),
                                  objective = h,
                                  state = stat)
                    db.session.add(tasks)
                return render_template('service/result.html')
    else:
        if request.form.get('run', None):
            host = request.form.getlist('run')
            for h in host:
                r = _nginx.delay(h, passwd=auth)
                stat = search(r)
                tasks = Tasks(uuid = str(r),
                              tasktouser = current_user.realname,
                              task = 'Nginx',
                              time = str(datetime.now()),
                              objective = h,
                              state = stat)
                db.session.add(tasks)
            return render_template('service/result.html')

    return render_template('service/nginx.html', hosts=hosts, pagination=pagination)


@service.route('/initredis', methods=['GET', 'POST'])
@login_required
def Redis():
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
            return render_template('service/redis.html', hosts=hosts, pagination=pagination)
        else:
            with open(key_file, 'w') as f:
                f.write(current_user.pri_key)
            if request.form.get('run', None):
                host = request.form.getlist('run')
                for h in host:
                    r = _redis.delay(h, passwd=None, key_filename=key_file)
                    stat = search(r)
                    tasks = Tasks(uuid = str(r),
                                  tasktouser = current_user.realname,
                                  task = 'Redis',
                                  time = str(datetime.now()),
                                  objective = h,
                                  state = stat)
                    db.session.add(tasks)
                return render_template('service/result.html')
    else:
        if request.form.get('run', None):
            host = request.form.getlist('run')
            for h in host:
                r = _redis.delay(h, passwd=auth)
                stat = search(r)
                tasks = Tasks(uuid = str(r),
                              tasktouser = current_user.realname,
                              task = 'Redis',
                              time = str(datetime.now()),
                              objective = h,
                              state = stat)
                db.session.add(tasks)
            return render_template('service/result.html')

    return render_template('service/redis.html', hosts=hosts, pagination=pagination)


@service.route('/initrabbitmq', methods=['GET', 'POST'])
@login_required
def Rabbitmq():
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
            return render_template('service/rabbitmq.html', hosts=hosts, pagination=pagination)
        else:
            with open(key_file, 'w') as f:
                f.write(current_user.pri_key)
            if request.form.get('run', None):
                host = request.form.getlist('run')
                for h in host:
                    r = _rabbitmq.delay(h, passwd=None, key_filename=key_file)
                    stat = search(r)
                    tasks = Tasks(uuid = str(r),
                                  tasktouser = current_user.realname,
                                  task = 'Rabbitmq',
                                  time = str(datetime.now()),
                                  objective = h,
                                  state = stat)
                    db.session.add(tasks)
                return render_template('service/result.html')
    else:
        if request.form.get('run', None):
            host = request.form.getlist('run')
            for h in host:
                r = _rabbitmq.delay(h, passwd=auth)
                stat = search(r)
                tasks = Tasks(uuid = str(r),
                              tasktouser = current_user.realname,
                              task = 'Rabbitmq',
                              time = str(datetime.now()),
                              objective = h,
                              state = stat)
                db.session.add(tasks)
            return render_template('service/result.html')

    return render_template('service/rabbitmq.html', hosts=hosts, pagination=pagination)


@service.route('/initmysql', methods=['GET', 'POST'])
@login_required
def Mysql():
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
            return render_template('service/mysql.html', hosts=hosts, pagination=pagination)
        else:
            with open(key_file, 'w') as f:
                f.write(current_user.pri_key)
            if request.form.get('run', None):
                host = request.form.getlist('run')
                for h in host:
                    r = _mysql.delay(h, passwd=None, key_filename=key_file)
                    stat = search(r)
                    tasks = Tasks(uuid = str(r),
                                  tasktouser = current_user.realname,
                                  task = 'Mysql',
                                  time = str(datetime.now()),
                                  objective = h,
                                  state = stat)
                    db.session.add(tasks)
                return render_template('service/result.html')
    else:
        if request.form.get('run', None):
            host = request.form.getlist('run')
            for h in host:
                r = _mysql.delay(h, passwd=auth)
                stat = search(r)
                tasks = Tasks(uuid = str(r),
                              tasktouser = current_user.realname,
                              task = 'Mysql',
                              time = str(datetime.now()),
                              objective = h,
                              state = stat)
                db.session.add(tasks)
            return render_template('service/result.html')

    return render_template('service/mysql.html', hosts=hosts, pagination=pagination)


@service.route('/upload', methods=['GET', 'POST'])
@login_required
def  upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('service.se'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


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
