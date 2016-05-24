#!/usr/bin/env python
# encoding: utf-8


import hashlib
from flask import render_template, redirect, url_for, abort, request, \
    current_app, flash
from . import main
from .forms import EditProfileForm, AddIdcForm, \
    EditGropuForm, AddGropuForm, EditIdcForm, AddHostForm, \
    EditHostForm
from .. import db
from ..models import User, IDC, Groups, Hosts
from flask.ext.login import login_required, current_user
from ..decorators import administrator_required


def encrypt(key):
    sha = hashlib.sha256()
    sha.update(key)
    return sha.hexdigest()


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    '''main page url'''
    return render_template('index.html')


@main.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    '''user information url'''
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    '''user information edit url'''
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.realname = form.realname.data
        current_user.mobile = form.mobile.data
        current_user.pub_key = form.pub_key.data
        current_user.pri_key = form.pri_key.data
        db.session.add(current_user)
        return redirect(url_for('.user', username=current_user.username))
    form.realname.data = current_user.realname
    form.mobile.data = current_user.mobile
    if current_user.pub_key is None:
        form.pub_key.data = current_user.pub_key
    else:
        form.pub_key.data = encrypt(current_user.pub_key)
    if current_user.pri_key is None:
        form.pri_key.data = current_user.pri_key
    else:
        form.pri_key.data = encrypt(current_user.pri_key)
    return render_template('edit_profile.html', form=form)


@main.route('/idc', methods=['GET', 'POST'])
@login_required
def idc():
    '''idc list for all'''
    page = request.args.get('page', 1, type=int)
    pagination = IDC.query.order_by(IDC.id.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'],
        error_out=False)
    idcs = pagination.items
    return render_template('idc.html',
                           pagination=pagination, idcs=idcs)


@main.route('/addidc', methods=['GET', 'POST'])
@login_required
@administrator_required
def addidc():
    form = AddIdcForm()
    if form.validate_on_submit():
        idc = IDC(name=form.name.data,
                  remark=form.remark.data)
        db.session.add(idc)
        return redirect(url_for('.idc'))
    return render_template('add_idc.html', form=form)


@main.route('/editidc/<int:id>', methods=['GET', 'POST'])
@login_required
@administrator_required
def edit_idc(id):
    idc = IDC.query.get_or_404(id)
    form = EditIdcForm(idc=idc)
    if form.validate_on_submit():
        idc.name = form.name.data
        idc.remark = form.remark.data
        db.session.add(idc)
        return redirect(url_for('.idc'))
    form.name.data = idc.name
    form.remark.data = idc.remark
    return render_template('edit_idc.html', form=form, idc=idc)


@main.route('/delidc/<int:id>', methods=['GET', 'POST'])
@login_required
@administrator_required
def del_idc(id):
    idc = IDC.query.get_or_404(id)
    if len(Hosts.query.join(IDC, Hosts.idc_id==id).all()) == 0:
        db.session.delete(idc)
        return redirect(url_for('.idc'))
    flash(u"请确保机房中没有主机存在.")
    return redirect(url_for('.idc'))


@main.route('/group', methods=['GET', 'POST'])
@login_required
def group():
    page = request.args.get('page', 1, type=int)
    pagination = Groups.query.order_by(Groups.id.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'],
        error_out=False)
    groups = pagination.items
    return render_template('group.html',
                           pagination=pagination, groups=groups)


@main.route('/addgroup', methods=['GET', 'POST'])
@login_required
@administrator_required
def addgroup():
    form = AddGropuForm()
    if form.validate_on_submit():
        group = Groups(name=form.name.data,
             remark=form.remark.data)
        db.session.add(group)
        return redirect(url_for('.group'))
    return render_template('add_group.html', form=form)


@main.route('/editgroup/<int:id>', methods=['GET', 'POST'])
@login_required
@administrator_required
def editgroup(id):
    group = Groups.query.get_or_404(id)
    form = EditGropuForm(group=group)
    if form.validate_on_submit():
        group.name = form.name.data
        group.remark = form.remark.data
        return redirect(url_for('.group'))
    form.name.data = group.name
    form.remark.data = group.remark
    return render_template('edit_group.html', form=form, group=group)


@main.route('/delgroup/<int:id>', methods=['GET', 'POST'])
@login_required
@administrator_required
def delgroup(id):
    group = Groups.query.get_or_404(id)
    if len(Hosts.query.join(Groups, Hosts.group_id==id).all()) == 0:
        db.session.delete(group)
        return redirect(url_for('.group'))
    flash(u"请确保组中没有主机存在.")
    return redirect(url_for('.group'))


@main.route('/host', methods=['GET', 'POST'])
@login_required
def host():
    page = request.args.get('page', 1, type=int)
    pagination = Hosts.query.order_by(Hosts.id.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'],
        error_out=False)
    hosts = pagination.items
    dictidc = {}
    dictgroup = {}
    for h in hosts:
        idcname = IDC.query.join(Hosts, IDC.id==h.idc_id).first()
        groupname = Groups.query.join(Hosts, Groups.id==h.group_id).first()
        dictidc[h.ip] = idcname
        dictgroup[h.ip] = groupname
    return render_template('host.html',
                           pagination=pagination, hosts=hosts,
                           dictidc=dictidc, dictgroup=dictgroup)


@main.route('/addhost', methods=['GET', 'POST'])
@login_required
@administrator_required
def addhost():
    form = AddHostForm()
    if form.validate_on_submit():
        host = Hosts(hostname=form.hostname.data,
                     ip=form.ip.data,
                     eip=form.eip.data,
                     system=form.system.data,
                     cpu=form.cpu.data,
                     mem=form.mem.data,
                     disk=form.disk.data,
                     group_id=form.groups.data,
                     idc_id=form.idc.data)
        db.session.add(host)
        return redirect(url_for('.host'))
    return render_template('add_host.html', form=form)


@main.route('/edithost/<int:id>', methods=['GET', 'POST'])
@login_required
@administrator_required
def edithost(id):
    host = Hosts.query.get_or_404(id)
    form = EditHostForm(host=host)
    if form.validate_on_submit():
        host.hostname = form.hostname.data
        host.ip = form.ip.data
        host.eip = form.eip.data
        host.system = form.system.data
        host.cpu = form.cpu.data
        host.mem = form.mem.data
        host.disk = form.disk.data
        host.group_id = form.groups.data
        host.idc_id = form.idc.data
        db.session.add(host)
        return redirect(url_for('.host'))
    form.hostname.data = host.hostname
    form.ip.data = host.ip
    form.eip.data = host.eip
    form.system.data = host.system
    form.cpu.data = host.cpu
    form.mem.data = host.mem
    form.disk.data = host.disk
    form.groups.data = host.group_id
    form.idc.data = host.idc_id
    return render_template('edit_host.html', form=form)


@main.route('/delhost/<int:id>', methods=['GET', 'POST'])
@login_required
@administrator_required
def delhost(id):
    host = Hosts.query.get_or_404(id)
    query = host.bind_user
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(User.id.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'],
        error_out=False)
    if len(pagination.items) == 0:
        db.session.delete(host)
        return redirect(url_for('.host'))
    flash(u"请确保该主机没有被其他用户绑定")
    return redirect(url_for('.host'))
