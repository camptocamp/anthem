# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)

from __future__ import print_function

import functools
import sys
import time

from past.builtins import PY3

from contextlib import contextmanager


def safe_print(ustring, errors='replace', **kwargs):
    """ Safely print a unicode string """
    encoding = sys.stdout.encoding or 'utf-8'
    if PY3:
        print(ustring, **kwargs)
    else:
        bytestr = ustring.encode(encoding, errors=errors)
        print(bytestr, **kwargs)


class LogIndent(object):

    def __init__(self):
        self.level = 0

    @contextmanager
    def display(self, name, timing=True, timestamp=False):
        self.print_indent(u'{}...'.format(name), timestamp=timestamp)
        self.level += 1
        start = time.time()
        try:
            yield
        except Exception:
            self.level -= 1
            self.print_indent(u'{}: error'.format(name), timestamp=timestamp)
            raise
        end = time.time()
        self.level -= 1
        if timing:
            self.print_indent(u"{}: {:.3f}s".format(name, end - start),
                              timestamp=timestamp)

    def print_indent(self, message, timestamp=False):
        if not timestamp:
            safe_print(u"{}{}".format(u"    " * self.level, message))
        else:
            safe_print(u"{}{}: {}".format(u"    " * self.level,
                                          time.strftime('%Y-%m-%d %H:%M:%S'),
                                          message))


def log(func=None, name=None, timing=True, timestamp=False):
    """ Decorator to show a description of the running function

    By default, it outputs the first line of the docstring.
    If the docstring is empty, it displays the name of the function.
    Alternatively, if a ``name`` is specified, it will display that only.

    It can be called as ``@log`` or as
    ``@log(name='abc, timing=True, timestamp=True)``.

    """
    # support to be called as @log or as @log(name='')
    if func is None:
        return functools.partial(log, name=name, timing=timing,
                                 timestamp=timestamp)

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
            message = func.__name__
        with ctx.log(message, timing=timing, timestamp=timestamp):
            return func(*args, **kwargs)
    return decorated
