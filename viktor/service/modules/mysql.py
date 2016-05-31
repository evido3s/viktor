#!/usr/bin/env python
# encoding: utf-8


from .. import celery
from ..executor import _exec
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@celery.task
def _mysql(host, passwd=None, key_filename=None):
    if passwd is None and key_filename is None:
        return False
    try:
        cmd = 'cd /tmp && wget -O mysql-repo.rpm http://repo.mysql.com//mysql57-community-release-el7-8.noarch.rpm \
            && yum localinstall mysql-repo.rpm && rm -rf mysql-repo.rpm \
            && yum-config-manager --disable mysql57-community \
            && yum-config-manager --enable mysql56-community \
            && yum install -y mysql-community-server && systemctl start mysqld'
        _exec(host, cmd, passwd, key_filename)
        return True
    except Exception, e:
        logger.exception(e)
        return False
