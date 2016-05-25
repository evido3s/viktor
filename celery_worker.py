#!/usr/bin/env python
# encoding: utf-8


from viktor import create_app, celery


app = create_app('default')
app.app_context().push()
