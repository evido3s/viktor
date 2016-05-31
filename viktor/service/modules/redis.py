#!/usr/bin/env python
# encoding: utf-8


from .. import celery
from ..executor import _exec
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@celery.task
def _redis(host, passwd=None, key_filename=None):
    if passwd is None and key_filename is None:
        return False
    try:
        cmd1 = 'yum install -y epel-release'
        cmd2 = "yum install -y redis && sed -i 's/^bind 127.0.0.1/bind 0.0.0.0/' /etc/redis.conf && systemctl restart redis || service redis restart"
        _exec(host, cmd1, passwd, key_filename)
        _exec(host, cmd2, passwd, key_filename)
        return True
    except Exception, e:
        logger.exception(e)
        return False
