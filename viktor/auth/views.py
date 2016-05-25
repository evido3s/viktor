#!/usr/bin/env python
# encoding: utf-8


from flask import render_template, redirect, request,\
    url_for, flash, current_app, jsonify
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User, Hosts
from .forms import LoginForm, ChangepasswordForm, AddUserForm, EditProfileAdminForm
from .. import db
from ..decorators import administrator_required


_THOUSAND_DAY = 86400 * 1000


@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''login route url'''
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        flash(u'用户名或密码无效.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/users', methods=['GET', 'POST'])
@login_required
@administrator_required
def users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.id.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'],
        error_out=False)
    users = pagination.items
    return render_template('auth/users.html',
            pagination=pagination, users=users)


@auth.route('/add_user', methods=['GET', 'POST'])
@login_required
@administrator_required
def add_user():
    '''admin can add a user'''
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    realname=form.realname.data,
                    mobile=form.mobile.data,
                    password=form.password.data)
        db.session.add(user)
        return redirect(url_for('auth.users'))
    return render_template('auth/add_user.html', form=form)


@auth.route('/bind_permission/<int:id>', methods=['GET', 'POST'])
@login_required
@administrator_required
def bindpermission(id):
    '''bind permission on user with host'''
    user = User.query.get_or_404(id)
    query = user.bind_host
    page = request.args.get('page', 1, type=int)
    pagination = Hosts.query.order_by(Hosts.ip.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'],
        error_out=False)
    exists = query.order_by(Hosts.ip.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'],
        error_out=False)
    hostip = list(set(pagination.items) - set(exists.items))

    if request.form.get('bindhost', None):
        h = request.form.getlist('bindhost')
        for k in h:
            b = Hosts.query.filter_by(ip=k).first()
            user.hosts.append(b)
        db.session.add(user)
        flash(u"绑定成功")
        return redirect(url_for('auth.users'))
    return render_template('auth/bindpermission.html', user=user,
                           pagination=pagination, hostip=hostip)


@auth.route('/unbindhost/<int:id>/<int:hid>', methods=['GET', 'POST'])
@login_required
@administrator_required
def unbindpermission(id, hid):
    '''user and host unbind '''
    user = User.query.get_or_404(id)
    host = Hosts.query.get_or_404(hid)
    user.hosts.remove(host)
    return redirect(url_for('auth.checkbindhost', id=id))


@auth.route('/checkbindlist/<int:id>', methods=['GET', 'POST'])
@login_required
@administrator_required
def checkbindhost(id):
    '''admin's ormal user bind host list'''
    user = User.query.get_or_404(id)
    query = user.bind_host
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Hosts.ip.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'],
        error_out=False)
    hosts = pagination.items
    return render_template('auth/check_bindhost.html', hosts=hosts,
                           pagination=pagination, user=user)


@auth.route('/userbind', methods=['GET', 'POST'])
@login_required
def normaluserbind():
    '''normal user bind itself host list'''
    user = User.query.get_or_404(current_user.id)
    query = user.bind_host
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Hosts.ip.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'],
        error_out=False)
    hosts = pagination.items
    return render_template('auth/check_bindhost.html', hosts=hosts,
                           pagination=pagination, user=user)


@auth.route('/sudo/<int:id>', methods=['GET', 'POST'])
@login_required
@administrator_required
def sudo(id):
    '''admin can give user administrator privileges'''
    user = User.query.get_or_404(id)
    if user.permissions != 0:
        user.permissions = 0
        db.session.add(user)
        return redirect(url_for('auth.users'))
    else:
        user.permissions = 1
        db.session.add(user)
        return redirect(url_for('auth.users'))


@auth.route('/editprofile/<int:id>', methods=['GET', 'POST'])
@login_required
@administrator_required
def edit_profile_admin(id):
    '''admin user information edit url'''
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.realname = form.realname.data
        user.mobile = form.mobile.data
        user.pub_key = form.pub_key.data
        user.pri_key = form.pri_key.data
        user.password = form.password.data
        db.session.add(user)
        return redirect(url_for('auth.users'))
    form.email.data = user.email
    form.username.data = user.username
    form.realname.data = user.realname
    form.mobile.data = user.mobile
    form.pub_key.data = user.pub_key
    form.pri_key.data = user.pri_key
    return render_template('edit_profile.html', form=form)


@auth.route('/del_user/<int:id>', methods=['GET', 'POST'])
@login_required
@administrator_required
def del_user(id):
    '''admin can del a user'''
    user =  User.query.get_or_404(id)
    query = user.bind_host
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Hosts.ip.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'],
        error_out=False)
    if len(pagination.items) == 0:
        db.session.delete(user)
        return redirect(url_for('auth.users'))
    flash(u"用户还绑定着主机")
    return redirect(url_for('auth.users'))


@auth.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    '''change password route url'''
    form = ChangepasswordForm()
    if request.method == "POST":
        if current_user.verify_password(form.oldpassword.data):
            current_user.password = form.newpassword.data
            db.session.add(current_user)
            flash(u'更改成功.')
            return redirect(url_for('main.index'))
        else:
            flash(u'更改失败.')
    return render_template("auth/changepassword.html",  form=form)
