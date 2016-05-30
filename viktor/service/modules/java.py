#!/usr/bin/env python
# encoding: utf-8


from .. import celery
from ..executor import _exec
from celery.utils.log import get_task_logger
from ..config import *


logger = get_task_logger(__name__)


@celery.task
def _java(host, uri, passwd=None, key_filename=None):
    if passwd is None and key_filename is None:
        return False
    try:
        cmd = 'cd /tmp && wget -P /tmp -O jdk-linux-x64.rpm %s && rpm -Uh /tmp/jdk-linux-x64.rpm 1>/dev/null' % uri
        _exec(host, cmd, passwd, key_filename)
        return True
    except Exception, e:
        logger.exception(e)
        return False
