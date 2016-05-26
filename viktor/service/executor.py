#!/usr/bin/env python
# encoding: utf-8


import paramiko
from datetime import datetime


def client(client, cmd):
    session = client.get_transport().open_session()
    try:
        session.exec_command(cmd)
    except Exception, e:
        "%s: %s" % (datetime.now(), e)
    exit_status = session.recv_exit_status()
    return exit_status == 0


def _exec(host, cmd, passwd=None, key_filename=None):
    clients = {}
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(
            host,
            username='root',
            password=passwd,
            key_filename=key_filename,
            look_for_keys=False,
        )
    except Exception, e:
        "%s: %s | %s" % (datetime.now(), host, e)
    else:
        clients[host] = client(ssh, cmd)

    return clients


def Upload(host, src, dst, passwd=None, pkey=None):
    try:
        scp = paramiko.Transport((host, 22))
        scp.connect(username='root', password=passwd, pkey=pkey)
        sftp = paramiko.SFTPClient.from_transport(scp)
        sftp.put(src, dst)
    except Exception, e:
        "%s: %s | %s" % (datetime.now(), host, e)
    finally:
        scp.close()
