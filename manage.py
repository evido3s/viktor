#!/usr/bin/env python
# encoding: utf-8


import os
from viktor import create_app, db
from viktor.models import User, IDC, Groups, Hosts
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.moment import Moment


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
moment = Moment(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, IDC=IDC, Groups=Groups, Hosts=Hosts)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
