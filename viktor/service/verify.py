#!/usr/bin/env python
# encoding: utf-8


import re
from .errors import IpError


def JudgeIP(ip):
    if re.findall(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', ip) == []:
        raise IpError('Invalid IP!(%s)' % ip)
