#!/usr/bin/env python
# encoding: utf-8


from .. import celery
from flask import current_app
from ..executor import Upload
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@celery.task
def _transfer(host, dst, passwd=None, key_filename=None):
    if passwd is None and key_filename is None:
        return False
    try:
        src
        Upload(host, dst, passwd, key_filename)
        return True
    except Exception, e:
        logger.exception(e)
        return False
