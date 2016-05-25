#!/usr/bin/env python
# encoding: utf-8


import random
import string
from celery.utils.log import get_task_logger
from .. import celery
from ..executor import _exec, Upload


logger = get_task_logger()


def _passwd(length=8):
    return ''.join([random.choice(string.ascii_letters+string.digits) for i in range(length)])


@celery.task
def update(host):
    cmd = 'yum update -y 1>/dev/null'
    _exec(host, cmd)
