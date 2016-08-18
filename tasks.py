# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)

from __future__ import print_function

import imp
import os

from invoke import task, Collection

ns = Collection()
tests = Collection('tests')
ns.add_collection(tests)

ODOO_URL = 'https://github.com/odoo/odoo/archive/{}.tar.gz'


@task
def tests_prepare(ctx, version='9.0'):
    try:
        imp.find_module('openerp')
    except ImportError:
        if not os.path.exists('odoo'):
            url = ODOO_URL.format(version)
            print('Getting {}'.format(url))
            ctx.run('wget -nv -c -O odoo.tar.gz {}'.format(url))
            ctx.run('tar xfz odoo.tar.gz')
            ctx.run('rm -f odoo.tar.gz')
            ctx.run('mv odoo-{} odoo'.format(version))
        print('Installing odoo')
        ctx.run('pip install -e odoo')


@task
def tests_createdb(ctx):
    print('Installing the database')
    ctx.run('odoo.py --stop-after-init')


@task
def tests_dropdb(ctx):
    print('Dropping the database')
    try:
        import openerp
        openerp.tools.config.parse_config(None)
        openerp.service.db.exp_drop('anthem-testdb')
    except ImportError:
        print('Could not import openerp')
        exit(1)


@task(default=True)
def tests_run(ctx):
    path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(path, 'tests', 'config', 'odoo.cfg')
    os.environ.setdefault('OPENERP_SERVER', config_path)
    ctx.run('tox', pty=True)


tests.add_task(tests_run, 'run')
tests.add_task(tests_createdb, 'createdb')
tests.add_task(tests_dropdb, 'dropdb')
tests.add_task(tests_prepare, 'prepare')
