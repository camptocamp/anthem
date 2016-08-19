# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)

from __future__ import print_function

import functools
import sys
import time

from contextlib import contextmanager


def safe_print(ustring, errors='replace', **kwargs):
    """ Safely print a unicode string """
    encoding = sys.stdout.encoding or 'utf-8'
    bytestr = ustring.encode(encoding, errors=errors)
    print(bytestr, **kwargs)


class LogIndent(object):

    def __init__(self):
        self.level = 0

    @contextmanager
    def display(self, name, timing=True):
        self.print_indent(u'{}...'.format(name))
        self.level += 1
        start = time.time()
        try:
            yield
        except:
            self.level -= 1
            self.print_indent(u'{}: error'.format(name))
            raise
        end = time.time()
        self.level -= 1
        if timing:
            self.print_indent(u"{}: {:.3f}s".format(name, end - start))

    def print_indent(self, message):
        safe_print(u"{}{}".format(u"    " * self.level, message))


def log(func=None, name=None, timing=True):
    """ Decorator to show a description of the running function

    By default, it outputs the first line of the docstring.
    If the docstring is empty, it displays the name of the function.
    Alternatively, if a ``name`` is specified, it will display that only.

    It can be called as ``@log`` or as ``@log(name='abc, timing=True)``.

    """
    # support to be called as @log or as @log(name='')
    if func is None:
        return functools.partial(log, name=name, timing=timing)

    @functools.wraps(func)
    def decorated(*args, **kwargs):
        assert len(args) > 0 and hasattr(args[0], 'log'), \
            "The first argument of the decorated function must be a Context"
        ctx = args[0]
        message = name
        if message is None:
            if func.__doc__:
                message = func.__doc__.splitlines()[0].strip()
        if message is None:
            message = func.func_name
        with ctx.log(message, timing=timing):
            return func(*args, **kwargs)
    return decorated
