#!/usr/bin/env python
# encoding: utf-8


from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import login_manager
from datetime import datetime


class Registrations(db.Model):
    user_id = db.Column(db.ForeignKey('users.id'), primary_key=True)
    host_id = db.Column(db.ForeignKey('hosts.id'), primary_key=True)


class User(UserMixin, db.Model):
    '''users for auth login'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    permissions = db.Column(db.Integer, nullable=False, default=1)
    pub_key = db.Column(db.Text)
    pri_key = db.Column(db.Text)
    realname = db.Column(db.String(64))
    mobile = db.Column(db.String(15))
    hosts = db.relationship('Hosts',
                            secondary=Registrations.__table__,
                            backref=db.backref('users', lazy='joined'),
                            lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username

    def admin(self):
        if self.permissions == 0:
            return True

    @property
    def bind_host(self):
        return Hosts.query.join(Registrations, Hosts.id==Registrations.host_id)\
            .filter(Registrations.user_id==self.id)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     realname=forgery_py.name.full_name(),
                     mobile=forgery_py.lorem_ipsum.sentences(randint(1, 20)))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def set_admin(passwd):
        u = User(email='test@admin.com',
                 username='admin',
                 password=passwd,
                 realname='administrator',
                 permissions=0)
        db.session.add(u)
        db.session.commit()


class IDC(db.Model):
    '''this is bgp data center'''
    __tablename__ = 'idc'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    remark = db.Column(db.Text(500))
    hosts = db.relationship('Hosts', backref='BGP')

    def __repr__(self):
        return self.name

    @staticmethod
    def generate_fake(count=3):
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            p = IDC(name=forgery_py.internet.user_name(True),
                    remark=forgery_py.lorem_ipsum.word() + '---test')
            db.session.add(p)
            db.session.commit()


class Groups(db.Model):
    '''Ucloud Business groups'''
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    remark = db.Column(db.Text(500))
    hosts = db.relationship('Hosts', backref='group')

    def __repr__(self):
        return self.name

    @staticmethod
    def generate_fake(count=10):
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            p = Groups(name=forgery_py.internet.user_name(True),
                       remark=forgery_py.lorem_ipsum.word() + '---test')
            db.session.add(p)
            db.session.commit()


class Hosts(db.Model):
    '''list of host'''
    __tablename__ = 'hosts'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(64), index=True, nullable=False)
    ip = db.Column(db.String(64), unique=True, index=True, nullable=False)
    eip = db.Column(db.String(64), index=True, nullable=True)
    system = db.Column(db.String(54), nullable=False)
    cpu = db.Column(db.Integer, nullable=False)
    mem = db.Column(db.Integer, nullable=False)
    disk = db.Column(db.Integer, nullable=True, default=0)
    create_time = db.Column(db.DateTime(), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
    idc_id = db.Column(db.Integer, db.ForeignKey('idc.id'))
    owned = db.relationship('User',
                            secondary=Registrations.__table__,
                            backref=db.backref('host', lazy='joined'),
                            lazy='dynamic')

    def __repr__(self):
        return self.ip

    @property
    def bind_user(self):
        return User.query.join(Registrations, User.id==Registrations.user_id)\
            .filter(Registrations.host_id==self.id)

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        from sqlalchemy.exc import IntegrityError
        import forgery_py

        seed()
        for i in range(count):
            h = Hosts(hostname=forgery_py.internet.user_name(True),
                      ip=forgery_py.internet.ip_v4(),
                      eip=forgery_py.internet.ip_v4(),
                      system='centos7',
                      cpu=randint(1, 8),
                      mem=randint(1, 32),
                      disk=randint(0, 5000),
                      create_time=datetime.now(),
                      idc_id=randint(1, 3),
                      group_id=randint(1, 5))
            db.session.add(h)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), unique=True, index=True, nullable=False)
    uuid = db.Column(db.String(64), unique=True, index=True, nullable=False)
    task = db.Column(db.String(32), nullable=False)
    time = db.Column(db.String(32), nullable=False)
    objective = db.Column(db.String(32), nullable=False)
    state = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return self.uuid


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
