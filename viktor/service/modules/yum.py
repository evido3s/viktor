#!/usr/bin/env python
# encoding: utf-8


from .. import celery
from ..executor import _exec
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@celery.task
def _install(host, package, passwd=None, key_filename=None):
    if passwd is None and key_filename is None:
        return False
    try:
        cmd = 'yum install -y %s' % package
        _exec(host, cmd, passwd, key_filename)
        return True
    except Exception, e:
        logger.exception(e)
        return False
