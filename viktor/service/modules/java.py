#!/usr/bin/env python
# encoding: utf-8


from .. import celery
from ..executor import _exec
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@celery.task
def _java(host, uri, passwd=None, key_filename=None):
    if passwd is None and key_filename is None:
        return False
    try:
        cmd = 'cd /tmp && wget -O jdk-linux-x64.rpm {link} && rpm -Uvh jdk-linux-x64.rpm && rm -rf jdk-linux-x64.rpm'.format( link=uri )
        _exec(host, cmd, passwd, key_filename)
        return True
    except Exception, e:
        logger.exception(e)
        return False
