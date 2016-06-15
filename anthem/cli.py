# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)
import argparse
import importlib

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
        'odoo-args',
        nargs=argparse.REMAINDER,
        help='command line arguments to be passed on to Odoo, like -c for a '
        'configuration file and -d for the database name. Those must be at '
        'the end of the arguments'
    )
    args = parser.parse_args()
    odoo_args = vars(args)['odoo-args']
    run(odoo_args, args.target)


def run(odoo_args, target):
    mod_name, func_name = target.split('::')
    module = importlib.import_module(mod_name)
    func = getattr(module, func_name)

    with Context(odoo_args) as ctx:
        func(ctx)
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
        openerp.service.server.start(preload=[], stop=True)
        dbname = openerp.tools.config['db_name']

        registry = openerp.modules.registry.RegistryManager.get(dbname)
        cr = registry.cursor()
        uid = openerp.SUPERUSER_ID
        Environment.reset()
        context = Environment(cr, uid, {})['res.users'].context_get()
        return Environment(cr, uid, context)
