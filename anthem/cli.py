# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)
import argparse
import code
import importlib

from anthem import __version__ as anthem_version
import openerp
from openerp.api import Environment


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
        'odoo-args',
        nargs=argparse.REMAINDER,
        help='command line arguments to be passed on to Odoo, like -c for a '
        'configuration file and -d for the database name. Those must be at '
        'the end of the arguments'
    )
    args = parser.parse_args()
    odoo_args = vars(args)['odoo-args']
    print(args)
    run(odoo_args, args.target, args.interactive)


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


def run(odoo_args, target, interactive):
    with Context(odoo_args) as ctx:
        mod_name, func_name = target.split('::')
        module = importlib.import_module(mod_name)
        func = getattr(module, func_name)
        func(ctx)
        if interactive:
            console = code.InteractiveConsole(locals={'ctx': ctx})
            import rlcompleter  # noqa
            import readline
            readline.parse_and_bind("tab: complete")
            console.interact(banner=banner())
        ctx.env.cr.commit()


class Context(object):
    def __init__(self, odoo_args):
        self.env = self._build_odoo_env(odoo_args)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.env.cr.close()

    def _build_odoo_env(self, odoo_args):
        openerp.tools.config.parse_config(odoo_args)
        dbname = openerp.tools.config['db_name']
        if not dbname:
            argparse.ArgumentParser().error(
                "please provide a database name though Odoo options (either "
                "-d or an Odoo configuration file)"
            )
        openerp.service.server.start(preload=[], stop=True)

        registry = openerp.modules.registry.RegistryManager.get(dbname)
        cr = registry.cursor()
        uid = openerp.SUPERUSER_ID
        Environment.reset()
        context = Environment(cr, uid, {})['res.users'].context_get()
        return Environment(cr, uid, context)
