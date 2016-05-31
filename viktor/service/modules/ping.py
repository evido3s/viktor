#!/usr/bin/env python
# encoding: utf-8


import subprocess
import shlex
from celery.utils.log import get_task_logger
from .. import celery


logger = get_task_logger(__name__)


@celery.task
def ping(host):
    cmd = "ping -c 2 %s" % host
    args = shlex.split(cmd)

    try:
        subprocess.check_call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False
