# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)

from __future__ import print_function

import argparse
import logging
import signal

from contextlib import contextmanager

try:
    import odoo
    from odoo.api import Environment
    odoo_logger = 'odoo'
except ImportError:
    # Odoo < 10.0
    import openerp as odoo  # noqa
    from openerp.api import Environment  # noqa
    odoo_logger = 'openerp'


from .output import LogIndent


class Options(object):

    def __init__(self, interactive=False, quiet=False, test_mode=False):
        self.interactive = interactive
        self.quiet = quiet
        self.test_mode = test_mode


class ContextMixin(object):

    def __init__(self, env, options=None):
        self.env = env
        self.options = options or Options()
        self._log = LogIndent()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def log_line(self, message):
        self._log.print_indent(message)

    @contextmanager
    def log(self, name, timing=True):
        if self.options.quiet:
            yield
        else:
            with self._log.display(name, timing=timing):
                yield


class Context(ContextMixin):
    """Standard context to call Odoo externally.

    Initialize Odoo connection using given Odoo configuration.
    """

    def __init__(self, odoo_args, options):
        env = self._build_odoo_env(odoo_args)
        options = options or Options()
        super(Context, self).__init__(env, options=options)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.options.test_mode:
            self.env.cr.rollback()
        self.env.cr.close()

    def _build_odoo_env(self, odoo_args):
        odoo.tools.config.parse_config(odoo_args)
        dbname = odoo.tools.config['db_name']
        if not dbname:
            argparse.ArgumentParser().error(
                "please provide a database name though Odoo options (either "
                "-d or an Odoo configuration file)"
            )
        logging.getLogger(odoo_logger).setLevel(logging.ERROR)
        odoo.service.server.start(preload=[], stop=True)

        # odoo.service.server.start() modifies the SIGINT signal by its own
        # one which in fact prevents us to stop anthem with Ctrl-c.
        # Restore the default one.
        signal.signal(signal.SIGINT, signal.default_int_handler)

        registry = odoo.modules.registry.RegistryManager.get(dbname)
        cr = registry.cursor()
        uid = odoo.SUPERUSER_ID
        Environment.reset()
        context = Environment(cr, uid, {})['res.users'].context_get()
        return Environment(cr, uid, context)


class ContextWithEnv(ContextMixin):
    """Context to run anthem in existing Odoo env.

    Usage:

        with ContextWithEnv(self.env) as ctx:
            my_song(ctx)
    """
