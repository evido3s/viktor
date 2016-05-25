#!/usr/bin/env python
# encoding: utf-8


class JayceError(Exception):

    def __init__(self, message=""):
        self.message = '%s' % str(message)

    def __str__(self):
        return self.message


class IpError(JayceError):
    pass

