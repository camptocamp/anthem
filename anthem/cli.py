# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)

from __future__ import print_function

import argparse
import code
import importlib
import logging
import signal

from contextlib import contextmanager

from anthem import __version__ as anthem_version
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


def main():
    parser = argparse.ArgumentParser(
        description='Anthem: make your Odoo scripts sing!')
    parser.add_argument(
        'target',
        help='the target to run in the format path.to.module::function. This '
        'will import path.to.module and run function'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='after playing the song, open an interactive console with access '
        'to ctx (the the Anthem context), much like running python -i'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Quiet the logs, which is sad for the songs.',
    )
    parser.add_argument(
        'odoo-args',
        nargs=argparse.REMAINDER,
        help='command line arguments to be passed on to Odoo, like -c for a '
        'configuration file and -d for the database name. Those must be at '
        'the end of the arguments'
    )
    args = parser.parse_args()
    odoo_args = vars(args)['odoo-args']
    options = Options(interactive=args.interactive, quiet=args.quiet)
    run(odoo_args, args.target, options)


def banner():
    b = (
        'Welcome to the anthem version {} interactive console!\n'
        '\n'
        'You can use an anthem context as ctx. (ctx.env is an Odoo\n'
        'environment). If you terminate your session with Ctrl-D,\n'
        'the database cursor ctx.env.cr will be committed.\n'
        'Otherwise if you exit() or you raise an exception, the cursor will\n'
        'be closed without a commit.\n'
    ).format(anthem_version)
    return b


class Options(object):

    def __init__(self, interactive=False, quiet=False, test_mode=False):
        self.interactive = interactive
        self.quiet = quiet
        self.test_mode = test_mode


def run(odoo_args, target, options):
    with Context(odoo_args, options) as ctx:
        mod_name, func_name = target.split('::')
        module = importlib.import_module(mod_name)
        func = getattr(module, func_name)
        func(ctx)
        if options.interactive:
            console = code.InteractiveConsole(locals={'ctx': ctx})
            import rlcompleter  # noqa
            import readline
            readline.parse_and_bind("tab: complete")
            console.interact(banner=banner())
        ctx.env.cr.commit()


class Context(object):
    def __init__(self, odoo_args, options):
        self.env = self._build_odoo_env(odoo_args)
        self.options = options
        self._log = LogIndent()

    def __enter__(self):
        return self

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

    def log_line(self, message):
        self._log.print_indent(message)

    @contextmanager
    def log(self, name, timing=True):
        if self.options.quiet:
            yield
        else:
            with self._log.display(name, timing=timing):
                yield
